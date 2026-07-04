from django.views.generic import ListView
from .models import BankOffer

class OfferListView(ListView):
    model = BankOffer
    template_name = 'offers/list.html'
    context_object_name = 'offers'
    paginate_by = 24

    def get_queryset(self):
        return BankOffer.objects.filter(is_active=True)
