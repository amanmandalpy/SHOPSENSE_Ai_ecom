from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from merchant_feeds.models import MerchantFeed, FeedStatus
from merchant_sync.models import MerchantImportJob, JobStatus
from merchant_sync.services.import_service import ImportService

@shared_task
def schedule_due_feeds():
    """
    Finds all active feeds that are due for synchronization and queues them.
    """
    now = timezone.now()
    due_feeds = MerchantFeed.objects.filter(
        status=FeedStatus.ACTIVE
    ).filter(
        next_sync__lte=now
    )
    
    for feed in due_feeds:
        execute_feed_import.delay(feed.id)

@shared_task
def execute_feed_import(feed_id):
    """
    Executes an import job for a given feed.
    """
    try:
        feed = MerchantFeed.objects.get(id=feed_id)
    except MerchantFeed.DoesNotExist:
        return
        
    # Prevent concurrent runs for the same feed
    if MerchantImportJob.objects.filter(feed=feed, status=JobStatus.RUNNING).exists():
        return
        
    job = MerchantImportJob.objects.create(
        merchant=feed.merchant,
        feed=feed,
        status=JobStatus.PENDING
    )
    
    # Calculate next sync early to prevent re-triggering
    if feed.sync_frequency > 0:
        feed.next_sync = timezone.now() + timedelta(minutes=feed.sync_frequency)
        feed.save(update_fields=['next_sync'])
        
    service = ImportService(job)
    service.execute()
