from django.contrib import admin
from django.urls import path

from pages.views import home_view, about_view, shoplist_view
from products.views import (
    product_detail_view,
    product_delete_view,
    product_list_view,
    product_update_view,
    product_create_view,
)

app_name = 'products'

urlpatterns = [
    path('<int:id>/delete/', product_delete_view, name="product-delete"),
    path('', product_list_view, name="product_list"),
    path('<int:id>/', product_detail_view, name="product-detail"),
    path('create/', product_create_view)
]