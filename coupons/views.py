from django.views.generic import ListView
from .models import Coupon, CouponStatus

class CouponListView(ListView):
    model = Coupon
    template_name = 'coupons/list.html'
    context_object_name = 'coupons'
    paginate_by = 24

    def get_queryset(self):
        return Coupon.objects.filter(status=CouponStatus.ACTIVE)
