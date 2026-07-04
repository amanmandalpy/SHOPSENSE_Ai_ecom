import os
import time
import requests
import tempfile
import json
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from django.utils.text import slugify

from brands.models import Brand
from categories.models import Category
from products.models import Product
from merchant_products.models import MerchantProduct, StockStatus
from merchant_sync.models import MerchantImportJob, MerchantSyncLog, MerchantImportError, JobStatus, LogLevel
from merchant_feeds.models import AuthType
from .feed_parser import FeedParserService
from .normalization import NormalizationService
from .duplicate_detection import DuplicateDetectionService

class ImportService:
    def __init__(self, job: MerchantImportJob):
        self.job = job
        self.feed = job.feed
        self.merchant = job.merchant
        self.detector = DuplicateDetectionService(self.merchant)
        
        # Caches
        self.brands_cache = {b.name.lower(): b for b in Brand.objects.all()}
        self.categories_cache = {c.name.lower(): c for c in Category.objects.all()}
        
    def execute(self):
        self.job.status = JobStatus.RUNNING
        self.job.started_at = timezone.now()
        self.job.save()
        
        start_time = time.time()
        temp_file = None
        
        try:
            self._log(LogLevel.INFO, f"Starting import for feed: {self.feed.name}")
            
            # 1. Download feed
            temp_file = self._download_feed()
            
            # 2. Parse and Process
            new_base_products = []
            new_merchant_products = []
            updates = []
            
            for index, raw_item in enumerate(FeedParserService.parse_feed(temp_file, self.feed.feed_type)):
                try:
                    norm = NormalizationService.normalize(raw_item)
                    
                    if not norm['sku'] or not norm['product_name']:
                        self.job.skipped_count += 1
                        continue
                        
                    if self.detector.is_merchant_product_duplicate(norm['sku']):
                        # We would handle updates here in a real scenario
                        # For simplicity, we just count as skipped/updated
                        self.job.updated_count += 1
                        continue
                        
                    # Find or Create Brand
                    brand = None
                    if norm['brand_name']:
                        b_key = norm['brand_name'].lower()
                        if b_key not in self.brands_cache:
                            brand = Brand.objects.create(name=norm['brand_name'], slug=slugify(norm['brand_name']))
                            self.brands_cache[b_key] = brand
                        else:
                            brand = self.brands_cache[b_key]
                            
                    # Find or Create Category
                    category = None
                    if norm['category_name']:
                        c_key = norm['category_name'].lower()
                        if c_key not in self.categories_cache:
                            category = Category.objects.create(name=norm['category_name'], slug=slugify(norm['category_name']))
                            self.categories_cache[c_key] = category
                        else:
                            category = self.categories_cache[c_key]
                            
                    # Base Product
                    base_product_id = self.detector.find_base_product(norm['product_name'], norm['brand_name'])
                    if not base_product_id:
                        # We must create it. We can't bulk_create if we need the ID immediately for MerchantProduct
                        # So we create it synchronously here (or we could chunk, but this is safer for exact mappings)
                        base_product = Product.objects.create(
                            name=norm['product_name'],
                            slug=slugify(norm['product_name'] + "-" + norm['sku']),
                            brand=brand,
                            category=category,
                            short_description=norm['description'] or '',
                            sku=norm['sku']
                        )
                        base_product_id = base_product.id
                        self.detector.register_new_base_product(norm['product_name'], norm['brand_name'], base_product_id)
                        
                    # Create Merchant Product
                    new_merchant_products.append(
                        MerchantProduct(
                            product_id=base_product_id,
                            merchant=self.merchant,
                            merchant_sku=norm['sku'],
                            merchant_product_url=norm['url'] or '',
                            merchant_price=Decimal(norm['price']) if norm['price'] else Decimal('0.00'),
                            original_price=Decimal(norm['original_price']) if norm['original_price'] else None,
                            stock=StockStatus.IN_STOCK if norm['stock'] == 'IN_STOCK' else StockStatus.OUT_OF_STOCK
                        )
                    )
                    
                    self.detector.register_new_merchant_sku(norm['sku'])
                    self.job.imported_count += 1
                    
                    # Batch insert every 500 records
                    if len(new_merchant_products) >= 500:
                        MerchantProduct.objects.bulk_create(new_merchant_products)
                        new_merchant_products.clear()
                        
                except Exception as e:
                    self.job.failed_count += 1
                    MerchantImportError.objects.create(
                        job=self.job,
                        raw_data=json.dumps(raw_item),
                        error_reason=str(e)
                    )
            
            # Final batch
            if new_merchant_products:
                MerchantProduct.objects.bulk_create(new_merchant_products)
                
            self.job.status = JobStatus.COMPLETED
            self._log(LogLevel.INFO, f"Import completed successfully.")
            
        except Exception as e:
            self.job.status = JobStatus.FAILED
            self._log(LogLevel.ERROR, f"Fatal error during import: {str(e)}")
            MerchantImportError.objects.create(
                job=self.job,
                raw_data="N/A",
                error_reason=f"FATAL: {str(e)}"
            )
        finally:
            # Only remove if it's actually a downloaded temp file (not the local file:// path)
            if temp_file and os.path.exists(temp_file) and not self.feed.feed_url.replace('file://', '') == temp_file:
                os.remove(temp_file)
                
            self.job.completed_at = timezone.now()
            self.job.duration_seconds = int(time.time() - start_time)
            self.job.save()
            
            # Update Feed Stats
            self.feed.last_sync = self.job.completed_at
            self.feed.imported_products = self.job.imported_count
            self.feed.failed_products = self.job.failed_count
            if self.job.status == JobStatus.COMPLETED:
                self.feed.status = 'ACTIVE'
            self.feed.save()

    def _download_feed(self):
        """Downloads feed to a temp file and returns path."""
        # For simplicity in this demo, if feed_url is a local file path (useful for testing), use it directly
        if self.feed.feed_url.startswith('file://') or os.path.exists(self.feed.feed_url):
            return self.feed.feed_url.replace('file://', '')
            
        auth = None
        if self.feed.auth_type == AuthType.BASIC:
            auth = (self.feed.username, self.feed.password)
            
        headers = {}
        if self.feed.auth_type == AuthType.BEARER:
            headers['Authorization'] = f"Bearer {self.feed.api_key}"
            
        response = requests.get(self.feed.feed_url, auth=auth, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        fd, path = tempfile.mkstemp(suffix=".feed")
        with os.fdopen(fd, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return path

    def _log(self, level, msg):
        MerchantSyncLog.objects.create(
            merchant=self.merchant,
            job=self.job,
            log_level=level,
            message=msg
        )
