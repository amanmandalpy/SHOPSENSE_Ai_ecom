from django.db import models
from affiliate.models import Merchant
from merchant_feeds.models import MerchantFeed

class JobStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RUNNING = 'RUNNING', 'Running'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'

class MerchantImportJob(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='import_jobs')
    feed = models.ForeignKey(MerchantFeed, on_delete=models.CASCADE, related_name='import_jobs')
    
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.PENDING)
    
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    imported_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    
    duration_seconds = models.IntegerField(default=0, help_text="Duration of the import in seconds")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Import Job #{self.pk} - {self.feed.name} ({self.status})"

class LogLevel(models.TextChoices):
    INFO = 'INFO', 'Information'
    WARNING = 'WARNING', 'Warning'
    ERROR = 'ERROR', 'Error'

class MerchantSyncLog(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='sync_logs')
    job = models.ForeignKey(MerchantImportJob, on_delete=models.CASCADE, related_name='logs', blank=True, null=True)
    
    log_level = models.CharField(max_length=10, choices=LogLevel.choices, default=LogLevel.INFO)
    message = models.CharField(max_length=500)
    error_details = models.TextField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"[{self.log_level}] {self.merchant.name} - {self.message[:50]}"

class MerchantImportError(models.Model):
    job = models.ForeignKey(MerchantImportJob, on_delete=models.CASCADE, related_name='import_errors')
    raw_data = models.TextField(help_text="Raw JSON or row data that failed")
    error_reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Error in Job #{self.job.pk} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
