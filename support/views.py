from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from .models import FAQCategory, FAQ, SupportTicket
from .forms import SupportTicketForm

class HelpCenterView(ListView):
    model = FAQCategory
    template_name = 'support/help_center.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return FAQCategory.objects.prefetch_related('faqs').all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            context['search_results'] = FAQ.objects.filter(
                Q(question__icontains=q) | Q(answer__icontains=q),
                is_published=True
            )
        return context

class SupportContactView(CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'support/contact.html'
    success_url = reverse_lazy('support_home')
    
    def form_valid(self, form):
        messages.success(self.request, "Your support ticket has been submitted. We will contact you soon.")
        return super().form_valid(form)
