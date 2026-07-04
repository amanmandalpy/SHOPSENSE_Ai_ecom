from django.db import models

class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome class e.g., 'fa-solid fa-book'")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'FAQ Categories'

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question

class SupportTicket(models.Model):
    TICKET_TYPES = [
        ('general', 'General Inquiry'),
        ('price_error', 'Report Incorrect Price'),
        ('broken_link', 'Report Broken Link'),
        ('product_error', 'Report Incorrect Product Information'),
        ('feature', 'Feature Request'),
        ('feedback', 'General Feedback'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=150)
    email = models.EmailField()
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES, default='general')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_ticket_type_display()}] {self.subject} - {self.email}"
