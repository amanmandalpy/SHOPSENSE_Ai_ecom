from decimal import Decimal
from django.utils import timezone
from django.db.models import Min, Max, Avg
from datetime import timedelta
from .models import PriceHistory

def record_price_change(merchant_product):
    """Records a new price history entry only if relevant data has changed."""
    last_record = PriceHistory.objects.filter(merchant_product=merchant_product).first()
    
    # Check if we need to write a new record
    if last_record:
        if (last_record.price == merchant_product.current_price and
            last_record.original_price == merchant_product.original_price and
            last_record.availability_status == merchant_product.stock and
            last_record.delivery_charge_snapshot == merchant_product.delivery_charge):
            return last_record # Nothing changed, avoid duplicate writes

    # Write new record
    new_record = PriceHistory.objects.create(
        merchant_product=merchant_product,
        price=merchant_product.current_price,
        original_price=merchant_product.original_price,
        currency=merchant_product.merchant.currency,
        availability_status=merchant_product.stock,
        seller_rating_snapshot=merchant_product.rating,
        delivery_charge_snapshot=merchant_product.delivery_charge,
        cashback_snapshot=False
    )
    return new_record

def get_price_statistics(merchant_product):
    """Calculates Lowest, Highest, Average and Trend data for a given merchant product."""
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    ninety_days_ago = now - timedelta(days=90)

    qs = PriceHistory.objects.filter(merchant_product=merchant_product)
    
    if not qs.exists():
        return None
        
    stats = {
        'current_price': merchant_product.merchant_price,
        'currency': merchant_product.merchant.currency,
        'all_time': qs.aggregate(
            lowest=Min('price'),
            highest=Max('price'),
            average=Avg('price')
        ),
        'thirty_days': qs.filter(recorded_at__gte=thirty_days_ago).aggregate(
            lowest=Min('price'),
            highest=Max('price')
        ),
        'ninety_days': qs.filter(recorded_at__gte=ninety_days_ago).aggregate(
            lowest=Min('price'),
            highest=Max('price')
        )
    }
    
    # Calculate drops
    highest = stats['all_time']['highest']
    if highest and highest > 0 and stats['current_price'] < highest:
        stats['price_drop_percentage'] = ((highest - stats['current_price']) / highest) * 100
    else:
        stats['price_drop_percentage'] = 0.0
        
    return stats
