from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product
from price_tracking.services import get_price_statistics
from offers.services import calculate_best_savings

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        qs = Product.objects.filter(status='ACTIVE')
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query) |
                Q(sku__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            
        # Filters
        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(brand__slug=brand)
            
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)
            
        return qs

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(status='ACTIVE').prefetch_related(
            'specifications', 
            'gallery_images', 
            'tags', 
            'related_products',
            'frequently_bought_together',
            'merchant_listings'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from recommendation.services import PersonalizationEngine
        PersonalizationEngine.log_product_view(self.request.user, self.object)
        
        from analytics.services import AnalyticsService
        from analytics.models import EventType
        AnalyticsService.log_event(EventType.PRODUCT_VIEW, user=self.request.user, metadata={'product_id': self.object.id})
        
        merchant_stats = []
        for listing in self.object.merchant_listings.all():
            stats = get_price_statistics(listing)
            savings = calculate_best_savings(listing)
            if stats:
                merchant_stats.append({
                    'listing': listing,
                    'stats': stats,
                    'savings': savings
                })
        context['merchant_stats'] = merchant_stats
        return context
