from django.urls import path
from .views import StoreListView, StoreDetailView

urlpatterns = [
    path('', StoreListView.as_view(), name='store_list'),
    path('<slug:slug>/', StoreDetailView.as_view(), name='store_detail'),
]
