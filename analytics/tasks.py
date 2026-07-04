from celery import shared_task
from .services import AnalyticsAggregationService

@shared_task
def aggregate_daily_analytics():
    """Run daily to aggregate clicks and views into MerchantAnalytics."""
    AnalyticsAggregationService.aggregate_daily_merchant_analytics()

@shared_task
def calculate_product_ctrs():
    """Run periodically to calculate CTRs for products."""
    AnalyticsAggregationService.calculate_product_ctrs()
