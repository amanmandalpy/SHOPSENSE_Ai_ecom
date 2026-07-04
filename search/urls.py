from django.urls import path
from .views import AdvancedSearchView

urlpatterns = [
    path('', AdvancedSearchView.as_view(), name='search_results'),
]
