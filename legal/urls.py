from django.urls import path
from .views import LegalDocumentView

urlpatterns = [
    path('<slug:slug>/', LegalDocumentView.as_view(), name='legal_document'),
]
