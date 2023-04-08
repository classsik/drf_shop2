from django.urls import path
from . import views


urlpatterns = [
    path('products', views.get_create_products),
    path('products/<int:pk>', views.get_edit_delete_product),
    path('cart', views.get_edit_cart),
    path('order', views.create_order)
]