from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from products.models import Product
from .services import (
    get_or_create_comparison_list,
    add_product_to_compare,
    remove_product_from_compare,
    clear_comparison_list,
    get_dynamic_comparison_matrix
)

class CompareView(TemplateView):
    template_name = 'comparison/compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comp_list = get_or_create_comparison_list(self.request)
        matrix_data = get_dynamic_comparison_matrix(comp_list)
        
        context['products'] = matrix_data['products']
        context['specifications'] = matrix_data['specifications']
        context['highlights'] = matrix_data['highlights']
        
        # Fallback empty state
        if not context['products']:
            context['trending_products'] = Product.objects.filter(status='ACTIVE')[:4]
            
        return context

def add_to_compare_view(request, product_id):
    try:
        add_product_to_compare(request, product_id)
        messages.success(request, "Product added to comparison.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect(request.META.get('HTTP_REFERER', 'compare_view'))

def remove_from_compare_view(request, product_id):
    remove_product_from_compare(request, product_id)
    messages.success(request, "Product removed from comparison.")
    return redirect('compare_view')

def clear_compare_view(request):
    clear_comparison_list(request)
    messages.success(request, "Comparison list cleared.")
    return redirect('compare_view')
