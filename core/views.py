from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
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
        page = self.kwargs.get('page', '')
        # Block non-HTML page names to avoid 500 errors (e.g. favicon.ico, robots.txt)
        if not page or '.' in page or len(page) > 50:
            raise Http404(f"Page '{page}' not found.")
        template_name = f'core/{page}.html'
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404(f"Page '{page}' not found.")
        return [template_name]

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

class NewsletterUnsubscribeView(View):
    def get(self, request, token):
        subscription = get_object_or_404(NewsletterSubscription, unsubscribe_token=token)
        subscription.is_active = False
        subscription.save()
        messages.success(request, "You have been successfully unsubscribed from our newsletter.")
        return redirect('home')


class FaviconView(View):
    """Serve favicon.ico — returns a minimal SVG favicon as ICO placeholder."""
    def get(self, request):
        # Serve the favicon as an SVG if the .ico file doesn't exist yet
        import os
        from django.conf import settings
        favicon_path = os.path.join(settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT or '', 'favicon.ico')
        if os.path.exists(favicon_path):
            with open(favicon_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/x-icon')
        # Fallback: return a tiny transparent 1×1 ICO
        # Minimal valid 1x1 transparent ICO file (bytes)
        ico_bytes = bytes([
            0,0,1,0,1,0,16,16,0,0,1,0,32,0,104,4,0,0,22,0,0,0,40,0,0,0,
            16,0,0,0,32,0,0,0,1,0,32,0,0,0,0,0,64,4,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0
        ] + [0]*1088)
        return HttpResponse(ico_bytes, content_type='image/x-icon')
