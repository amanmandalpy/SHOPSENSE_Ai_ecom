from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from recommendation.services import PersonalizationEngine
from .models import NewsletterSubscription
from .forms import ContactForm, NewsletterForm

class HomeView(View):
    def get(self, request):
        context = {
            'trending_deals': PersonalizationEngine.get_trending_deals(limit=8)
        }
        
        if request.user.is_authenticated:
            context['recently_viewed'] = PersonalizationEngine.get_recently_viewed(request.user, limit=8)
            context['recommended_for_you'] = PersonalizationEngine.get_recommended_for_you(request.user, limit=8)
            
        return render(request, 'core/index.html', context)

class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({
            'status': 'ok',
            'service': 'ShopSense AI v1.0.0',
            'version': '1.0.0'
        }, status=200)

class PublicPageView(TemplateView):
    def get_template_names(self):
        return [f'core/{self.kwargs["page"]}.html']

class ContactView(CreateView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent successfully! Our team will get back to you shortly.")
        return super().form_valid(form)

class NewsletterSubscribeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            obj, created = NewsletterSubscription.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Successfully subscribed to the newsletter!")
            else:
                messages.info(request, "You are already subscribed to the newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")
        
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)

from django.shortcuts import get_object_or_404

class NewsletterUnsubscribeView(View):
    def get(self, request, token):
        subscription = get_object_or_404(NewsletterSubscription, unsubscribe_token=token)
        subscription.is_active = False
        subscription.save()
        messages.success(request, "You have been successfully unsubscribed from our newsletter.")
        return redirect('home')
