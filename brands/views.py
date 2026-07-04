from django.views.generic import ListView, DetailView
from .models import Brand

class BrandListView(ListView):
    model = Brand
    template_name = 'brands/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 24
    
    def get_queryset(self):
        return Brand.objects.filter(is_active=True)

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brands/brand_detail.html'
    context_object_name = 'brand'
    
    def get_queryset(self):
        return Brand.objects.filter(is_active=True)
