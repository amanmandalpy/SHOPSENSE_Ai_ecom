from decimal import Decimal
from coupons.models import Coupon, DiscountType as CouponDiscountType
from .models import BankOffer, DiscountType as OfferDiscountType

def calculate_best_savings(merchant_listing):
    """
    Calculates the absolute lowest effective price based on applicable Coupons and Bank Offers.
    merchant_listing: MerchantProduct instance
    """
    current_price = merchant_listing.current_price
    store = merchant_listing.store
    
    # 1. Evaluate Best Coupon
    coupons = Coupon.objects.filter(store=store)
    best_coupon = None
    max_coupon_saving = Decimal('0.00')
    
    for coupon in coupons:
        if coupon.is_valid() and current_price >= coupon.min_order_value:
            saving = Decimal('0.00')
            if coupon.discount_type == CouponDiscountType.FLAT:
                saving = coupon.discount_value
            elif coupon.discount_type == CouponDiscountType.PERCENTAGE:
                saving = (current_price * coupon.discount_value) / Decimal('100')
                if coupon.max_discount and saving > coupon.max_discount:
                    saving = coupon.max_discount
            
            if saving > max_coupon_saving:
                max_coupon_saving = saving
                best_coupon = coupon

    # Intermediate price after coupon
    price_after_coupon = current_price - max_coupon_saving
    
    # 2. Evaluate Best Bank Offer
    # Bank Offers can be specific to Store or global (store is null)
    bank_offers = BankOffer.objects.filter(store=store) | BankOffer.objects.filter(store__isnull=True)
    best_bank_offer = None
    max_bank_saving = Decimal('0.00')
    
    for offer in bank_offers:
        # Bank minimum order value usually applies to price before bank discount but after coupons
        if offer.is_valid() and price_after_coupon >= offer.min_order_value:
            saving = Decimal('0.00')
            if offer.discount_type == OfferDiscountType.FLAT:
                saving = offer.discount_value
            elif offer.discount_type == OfferDiscountType.PERCENTAGE:
                saving = (price_after_coupon * offer.discount_value) / Decimal('100')
                if offer.max_discount and saving > offer.max_discount:
                    saving = offer.max_discount
            
            if saving > max_bank_saving:
                max_bank_saving = saving
                best_bank_offer = offer

    final_effective_price = price_after_coupon - max_bank_saving
    total_savings = current_price - final_effective_price
    
    return {
        'original_price': merchant_listing.original_price or current_price,
        'current_price': current_price,
        'best_coupon': best_coupon,
        'coupon_savings': max_coupon_saving,
        'best_bank_offer': best_bank_offer,
        'bank_savings': max_bank_saving,
        'final_effective_price': max(Decimal('0.00'), final_effective_price),
        'total_savings': total_savings
    }
