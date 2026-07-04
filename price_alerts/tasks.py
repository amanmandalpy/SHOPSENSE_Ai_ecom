from celery import shared_task
from django.utils import timezone
from .models import PriceAlert, AlertStatus, AlertType
from notifications.services import send_notification
from notifications.models import NotificationType

@shared_task
def process_active_price_alerts():
    """
    Scans all active Price Alerts.
    If the underlying merchant product price meets the trigger condition, it fires a notification.
    """
    active_alerts = PriceAlert.objects.filter(status=AlertStatus.ACTIVE).select_related('merchant_product', 'user', 'merchant_product__product', 'merchant_product__store')
    
    triggered_count = 0
    now = timezone.now()
    
    for alert in active_alerts:
        product_name = alert.merchant_product.product.name
        store_name = alert.merchant_product.store.name
        current_price = alert.merchant_product.current_price
        
        trigger = False
        message = ""
        
        if alert.alert_type == AlertType.BELOW_TARGET:
            if current_price <= alert.target_price:
                trigger = True
                message = f"Great news! {product_name} at {store_name} has dropped to {alert.currency} {current_price}, which is below your target of {alert.currency} {alert.target_price}."
                
        if trigger:
            alert.status = AlertStatus.TRIGGERED
            alert.triggered_at = now
            alert.notification_sent = True
            alert.save()
            
            send_notification(
                user=alert.user,
                title=f"Price Alert Triggered: {product_name}",
                message=message,
                notification_type=NotificationType.PRICE_ALERT,
                action_url=alert.merchant_product.get_absolute_url()
            )
            triggered_count += 1
            
    return f"Processed active alerts. Triggered {triggered_count} notifications."
