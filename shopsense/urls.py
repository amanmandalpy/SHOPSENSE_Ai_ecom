from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('brands/', include('brands.urls')),
    path('stores/', include('stores.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('products.urls')),
    path('merchants/', include('merchant_products.urls')),
]
