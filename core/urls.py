from django.urls import path
from .views import HomeView, HealthCheckView, PublicPageView, ContactView, NewsletterSubscribeView, NewsletterUnsubscribeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/health/', HealthCheckView.as_view(), name='health_check'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<uuid:token>/', NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
    path('<str:page>/', PublicPageView.as_view(), name='public_page'),
]
