from accounts.models import User
from products.models import Product, Brand, Category
from stores.models import Store
from merchant_products.models import MerchantProduct
from ai_assistant.models import AILog
from wishlist.models import WishlistItem
from core.models import NewsletterSubscription
from support.models import SupportTicket
from django.utils import timezone
from datetime import timedelta

def admin_dashboard_stats(request):
    # Only calculate stats for the admin homepage to avoid overhead
    if request.path != '/admin/' or not request.user.is_superuser:
        return {}
        
    today = timezone.now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()
        
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'new_users_today': new_users_today,
        'total_products': Product.objects.count(),
        'total_brands': Brand.objects.count(),
        'total_categories': Category.objects.count(),
        'total_stores': Store.objects.count(),
        'total_merchant_products': MerchantProduct.objects.count(),
        'total_ai_requests': AILog.objects.count(),
        'total_wishlists': WishlistItem.objects.count(),
        'total_newsletters': NewsletterSubscription.objects.count(),
        'total_support_tickets': SupportTicket.objects.count(),
        'open_support_tickets': SupportTicket.objects.filter(status__in=['new', 'in_progress']).count(),
    }
    
    return {'bos_stats': stats}
