from django.urls import path
from .views import product, productInfo, cart_view, add_to_wishlist, Remove_from_Wishlist, add_to_cart, remove_from_cart, checkout_page, address_page, delete_address, order_success, back_to_home



urlpatterns = [path("", product, name = "product"),
               path("productInfo/<int:product_id>/",productInfo,name="productInfo"),
               path("cart_view/", cart_view, name="cart_view"),
               path("add-wishlist/<int:product_id>/",add_to_wishlist, name="add_to_wishlist"),
               path("remove-wishlist/<int:product_id>/",Remove_from_Wishlist, name="Remove_from_Wishlist"),
               path("add_to_cart/<int:product_id>/",add_to_cart, name="add_to_cart"),
               path("remove_from_cart/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
               path("checkout/", checkout_page, name="checkout_page"),
               path("address/", address_page, name="address"),
               path("delete_address/<int:address_id>/",delete_address, name="delete_address"),
               path('order_success/', order_success, name='order_success'),
               path('back_to_home/', back_to_home, name='back_to_home')]