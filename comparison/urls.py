from django.urls import path
from .views import CompareView, add_to_compare_view, remove_from_compare_view, clear_compare_view

urlpatterns = [
    path('', CompareView.as_view(), name='compare_view'),
    path('add/<int:product_id>/', add_to_compare_view, name='add_to_compare'),
    path('remove/<int:product_id>/', remove_from_compare_view, name='remove_from_compare'),
    path('clear/', clear_compare_view, name='clear_compare'),
]
