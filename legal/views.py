from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import LegalDocument

class LegalDocumentView(DetailView):
    model = LegalDocument
    template_name = 'legal/document.html'
    context_object_name = 'document'
    
    def get_object(self):
        return get_object_or_404(LegalDocument, slug=self.kwargs['slug'], is_published=True)
