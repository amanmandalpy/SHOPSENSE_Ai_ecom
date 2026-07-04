from django.db import models

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class SiteSettings(SingletonModel):
    # General
    website_name = models.CharField(max_length=100, default='ShopSense AI')
    logo = models.ImageField(upload_to='system/', blank=True, null=True)
    favicon = models.ImageField(upload_to='system/', blank=True, null=True)
    currency = models.CharField(max_length=10, default='USD')
    language = models.CharField(max_length=10, default='en-US')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Modes
    maintenance_mode = models.BooleanField(default=False)
    registration_enabled = models.BooleanField(default=True)
    email_verification_required = models.BooleanField(default=False)
    
    # SMTP Settings
    smtp_host = models.CharField(max_length=255, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_user = models.CharField(max_length=255, blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)
    smtp_use_tls = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return "Global Site Settings"

class SystemLog(models.Model):
    LOG_LEVELS = [
        ('info', 'INFO'),
        ('warning', 'WARNING'),
        ('error', 'ERROR'),
        ('critical', 'CRITICAL')
    ]
    level = models.CharField(max_length=20, choices=LOG_LEVELS, default='info')
    module = models.CharField(max_length=100)
    message = models.TextField()
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_level_display()}] {self.module} - {self.created_at}"

class HomepageBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
