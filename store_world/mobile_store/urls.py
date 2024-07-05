from django.urls import path
from .views import product, productInfo


urlpatterns = [path("", product, name = "product"),
               path("productInfo/<int:product_id>/",productInfo,name="productInfo")]