from django.views.generic import ListView, DetailView
from .models import Store

class StoreListView(ListView):
    model = Store
    template_name = 'stores/store_list.html'
    context_object_name = 'stores'
    paginate_by = 12

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'name')
        qs = Store.objects.filter(is_active=True)
        if sort == 'rating':
            qs = qs.order_by('-rating')
        elif sort == 'new':
            qs = qs.order_by('-created_at')
        return qs

class StoreDetailView(DetailView):
    model = Store
    template_name = 'stores/store_detail.html'
    context_object_name = 'store'

    def get_queryset(self):
        return Store.objects.filter(is_active=True)
