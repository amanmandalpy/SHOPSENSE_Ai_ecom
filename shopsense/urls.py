from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from seo import views as seo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('brands/', include('brands.urls')),
    path('stores/', include('stores.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('products.urls')),
    path('merchants/', include('merchant_products.urls')),
    path('alerts/', include('price_alerts.urls')),
    path('notifications/', include('notifications.urls')),
    path('search/', include('search.urls')),
    path('compare/', include('comparison.urls')),
    path('coupons/', include('coupons.urls')),
    path('offers/', include('offers.urls')),
    path('ai/', include('ai_assistant.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('out/', include('affiliate.urls')),
    path('support/', include('support.urls')),
    path('legal/', include('legal.urls')),
    path('sys/', include('system.urls')),
    path('robots.txt', seo_views.robots_txt),
    path('sitemap.xml', seo_views.sitemap_xml),
    path('', include('core.urls')),
]
