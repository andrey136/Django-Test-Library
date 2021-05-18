from django.contrib import admin
from django.urls import path
from products.views import products_list_view, products_detail_view, products_create_view

urlpatterns = [
    path('', products_list_view, name="products_list"),
    path('<int:id>/', products_detail_view, name="product_detail"),
    path('create/', products_create_view, name="product_create")
]

app_name='products'