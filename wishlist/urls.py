from django.urls import path
from .views import WishlistView, AddToWishlistView, RemoveFromWishlistView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist_home'),
    path('add/<int:product_id>/', AddToWishlistView.as_view(), name='wishlist_add'),
    path('remove/<int:item_id>/', RemoveFromWishlistView.as_view(), name='wishlist_remove'),
]
