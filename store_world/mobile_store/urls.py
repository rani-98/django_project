from django.urls import path
from .views import product, productInfo,cart


urlpatterns = [path("", product, name = "product"),
               path("productInfo/<int:product_id>/",productInfo,name="productInfo"),
               path("cart/", cart, name="cart")]