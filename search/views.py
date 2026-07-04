from django.views.generic import ListView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from products.models import Product
from .services import execute_search, log_search
from categories.models import Category
from brands.models import Brand
from stores.models import Store

@method_decorator(ratelimit(key='ip', rate='20/m', block=True), name='dispatch')
class AdvancedSearchView(ListView):
    template_name = 'search/search_results.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        query_string = self.request.GET.get('q', '')
        
        filters = {
            'category': self.request.GET.get('category'),
            'brand': self.request.GET.get('brand'),
            'store': self.request.GET.get('store'),
            'min_price': self.request.GET.get('min_price'),
            'max_price': self.request.GET.get('max_price'),
        }
        sort_by = self.request.GET.get('sort_by')
        
        qs = execute_search(query_string, filters, sort_by)
        
        # Log analytics asynchronously (synchronous for now)
        log_search(query_string, qs.count())
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.filter(is_active=True)
        context['brands'] = Brand.objects.all()
        context['stores'] = Store.objects.filter(is_active=True)
        
        # Keep track of active filters
        context['active_category'] = self.request.GET.get('category', '')
        context['active_brand'] = self.request.GET.get('brand', '')
        context['active_store'] = self.request.GET.get('store', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        
        # Fallback empty state
        if not context['products']:
            context['trending_products'] = Product.objects.filter(status='ACTIVE')[:4]
            
        return context
