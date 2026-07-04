from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from analytics.models import PlatformEvent, EventType
from products.models import Product
from wishlist.models import WishlistItem

class AdminDashboardView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        total_searches = PlatformEvent.objects.filter(event_type=EventType.SEARCH).count()
        total_ai_queries = PlatformEvent.objects.filter(event_type=EventType.AI_QUERY).count()
        total_product_views = PlatformEvent.objects.filter(event_type=EventType.PRODUCT_VIEW).count()
        
        top_wishlisted = Product.objects.annotate(
            wishlist_count=Count('wishlistitem')
        ).filter(wishlist_count__gt=0).order_by('-wishlist_count')[:10]
        
        recent_events = PlatformEvent.objects.all()[:15]

        context = {
            'total_searches': total_searches,
            'total_ai_queries': total_ai_queries,
            'total_product_views': total_product_views,
            'top_wishlisted': top_wishlisted,
            'recent_events': recent_events
        }
        return render(request, 'dashboard/index.html', context)
