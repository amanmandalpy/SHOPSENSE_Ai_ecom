from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from analytics.models import MerchantAnalytics, ProductAnalytics, PlatformEvent, EventType
from tracking.models import AffiliateClick
from merchant_products.models import MerchantProduct
from products.models import Product

class AnalyticsAggregationService:
    @staticmethod
    def aggregate_daily_merchant_analytics(date=None):
        if date is None:
            date = timezone.now().date() - timedelta(days=1)
            
        # Group clicks by merchant
        merchants = AffiliateClick.objects.filter(click_timestamp__date=date).values('merchant').annotate(
            total_clicks=Count('id'),
            unique_clicks=Count('session', distinct=True)
        )
        
        for item in merchants:
            merchant_id = item['merchant']
            if not merchant_id:
                continue
                
            MerchantAnalytics.objects.update_or_create(
                merchant_id=merchant_id,
                date=date,
                defaults={
                    'total_clicks': item['total_clicks'],
                    'unique_clicks': item['unique_clicks']
                }
            )

    @staticmethod
    def calculate_product_ctrs():
        views = PlatformEvent.objects.filter(event_type=EventType.PRODUCT_VIEW)
        views_dict = {}
        for v in views:
            meta = v.metadata
            if isinstance(meta, str):
                import json
                try: meta = json.loads(meta.replace("'", '"'))
                except: meta = {}
            if not isinstance(meta, dict):
                meta = {}
            pid = str(meta.get('product_id', ''))
            if pid.isdigit():
                views_dict[pid] = views_dict.get(pid, 0) + 1
                
        clicks = AffiliateClick.objects.values('product_id').annotate(count=Count('id'))
        clicks_dict = {str(item['product_id']): item['count'] for item in clicks if item['product_id']}
        
        all_product_ids = set(list(views_dict.keys()) + list(clicks_dict.keys()))
        
        for pid in all_product_ids:
            if not pid.isdigit(): continue
            view_count = views_dict.get(pid, 0)
            click_count = clicks_dict.get(pid, 0)
            
            pa, _ = ProductAnalytics.objects.get_or_create(product_id=int(pid))
            pa.views_count = view_count
            pa.affiliate_clicks = click_count
            pa.calculate_ctr()

class AnalyticsService:
    @staticmethod
    def log_event(event_type, user=None, metadata=None):
        from analytics.models import PlatformEvent
        if metadata is None: metadata = {}
        PlatformEvent.objects.create(
            event_type=event_type,
            user=user if getattr(user, 'is_authenticated', False) else None,
            metadata=metadata
        )
