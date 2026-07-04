from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Notification

class NotificationCenterView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_center.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

def mark_notification_read(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.action_url:
        return redirect(notif.action_url)
    return redirect('notification_center')
