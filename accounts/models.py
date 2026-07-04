from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
    ADMIN = 'ADMIN', _('Admin')
    CUSTOMER = 'CUSTOMER', _('Customer')
    MODERATOR = 'MODERATOR', _('Moderator')
    CONTENT_MANAGER = 'CONTENT_MANAGER', _('Content Manager')
    AFFILIATE_MANAGER = 'AFFILIATE_MANAGER', _('Affiliate Manager')

class GenderChoices(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')
    PREFER_NOT_TO_SAY = 'X', _('Prefer not to say')

class User(AbstractUser):
    """
    Custom user model supporting advanced roles and extended profile data.
    """
    # Identity & Roles
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        help_text=_('Designates the primary role of the user.')
    )
    email_verified = models.BooleanField(
        default=False,
        help_text=_('Designates whether this user has verified their email address.')
    )

    # Extended Profile
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Location & Preferences
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='en', blank=True)
    preferred_currency = models.CharField(max_length=10, default='INR', blank=True)
    timezone = models.CharField(max_length=50, default='UTC', blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
