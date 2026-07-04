from django import forms
from .models import ContactMessage, NewsletterSubscription

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
