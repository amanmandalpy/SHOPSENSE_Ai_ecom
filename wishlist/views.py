from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Wishlist, WishlistItem
from products.models import Product

class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user, name='My Wishlist')
        items = wishlist.items.select_related('product').all()
        
        # Map products to their best active listings
        mapped_items = []
        for item in items:
            listing = item.product.merchant_listings.first()
            if listing:
                mapped_items.append({'item': item, 'listing': listing})
                
        return render(request, 'wishlist/index.html', {'mapped_items': mapped_items})

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user, name='My Wishlist')
        
        obj, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        if created:
            from analytics.services import AnalyticsService
            from analytics.models import EventType
            AnalyticsService.log_event(EventType.WISHLIST_ADD, user=request.user, metadata={'product_id': product.id})
            messages.success(request, f"{product.name} added to your wishlist!")
        else:
            messages.info(request, f"{product.name} is already in your wishlist.")
            
        return redirect(request.META.get('HTTP_REFERER', 'home'))

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(WishlistItem, pk=item_id, wishlist__user=request.user)
        item.delete()
        messages.success(request, "Item removed from wishlist.")
        return redirect('wishlist_home')
