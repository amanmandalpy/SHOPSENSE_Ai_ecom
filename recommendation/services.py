from user_preferences.models import BrowsingHistory, UserPreference
from merchant_products.models import MerchantProduct
from ai_assistant.scoring import ShoppingScoreService
from products.models import Product

class PersonalizationEngine:
    @staticmethod
    def log_product_view(user, product):
        if not user.is_authenticated:
            return
            
        # Update or create viewing history
        obj, created = BrowsingHistory.objects.update_or_create(
            user=user,
            product=product,
            defaults={} # viewed_at auto updates
        )
        
        # Enforce performance limit: 50 items max per user history
        history_count = BrowsingHistory.objects.filter(user=user).count()
        if history_count > 50:
            # Delete oldest
            oldest_ids = BrowsingHistory.objects.filter(user=user).order_by('-viewed_at')[50:].values_list('id', flat=True)
            BrowsingHistory.objects.filter(id__in=list(oldest_ids)).delete()

    @staticmethod
    def get_recently_viewed(user, limit=5):
        if not user.is_authenticated:
            return []
            
        history = BrowsingHistory.objects.filter(user=user).select_related('product')[:limit]
        products = [h.product for h in history]
        
        listings = []
        for p in products:
            listing = p.merchant_listings.first()
            if listing:
                listings.append(listing)
        return listings

    @staticmethod
    def get_recommended_for_you(user, limit=5):
        if not user.is_authenticated:
            return []
            
        # Map user's recent categories
        recent_cats = BrowsingHistory.objects.filter(user=user).values_list('product__category', flat=True)[:10]
        recent_cats = list(set(recent_cats))
        
        if not recent_cats:
            return []
            
        # Grab active products from these categories that the user hasn't viewed yet
        recommended_products = Product.objects.filter(category__in=recent_cats, status='ACTIVE')\
            .exclude(browsing_history__user=user)\
            .order_by('-created_at')[:limit*2]
            
        listings = []
        for p in recommended_products:
            listing = p.merchant_listings.first()
            if listing:
                listings.append(listing)
                
        # Sort aggressively by active Savings score
        listings.sort(key=lambda x: ShoppingScoreService.calculate_score(x), reverse=True)
        return listings[:limit]

    @staticmethod
    def get_trending_deals(limit=5):
        recent_products = Product.objects.filter(status='ACTIVE').order_by('-created_at')[:20]
        
        listings = []
        for p in recent_products:
            listing = p.merchant_listings.first()
            if listing:
                listings.append(listing)
                
        # Rank by current dynamic price discount
        listings.sort(key=lambda x: ShoppingScoreService.calculate_score(x), reverse=True)
        return listings[:limit]
