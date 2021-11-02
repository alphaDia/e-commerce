from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>',
         views.add_cart_item, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>',
         views.remove_cart_item, name='remove_from_cart'),
    path('remove_product_from_cart_item/<int:product_id>',
         views.remove_product_from_cart, name='remove_product_from_cart_item'),

]
