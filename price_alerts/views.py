from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import PriceAlert, AlertStatus

class MyAlertsView(LoginRequiredMixin, ListView):
    model = PriceAlert
    template_name = 'price_alerts/my_alerts.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

class PriceAlertCreateView(LoginRequiredMixin, CreateView):
    model = PriceAlert
    fields = ['merchant_product', 'target_price']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, "Failed to create alert. You may already have one active for this product.")
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        messages.success(self.request, "Price alert created successfully!")
        return self.request.META.get('HTTP_REFERER', '/')

def toggle_alert_status(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    alert = get_object_or_404(PriceAlert, pk=pk, user=request.user)
    if alert.status == AlertStatus.ACTIVE:
        alert.status = AlertStatus.PAUSED
    elif alert.status == AlertStatus.PAUSED:
        alert.status = AlertStatus.ACTIVE
    alert.save()
    messages.success(request, f"Alert status updated to {alert.status}.")
    return redirect('my_alerts')

def delete_alert(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    alert = get_object_or_404(PriceAlert, pk=pk, user=request.user)
    alert.delete()
    messages.success(request, "Alert deleted.")
    return redirect('my_alerts')
