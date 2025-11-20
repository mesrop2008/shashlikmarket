from django.contrib import admin
from django.urls import path
from shashlikmarket.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('menu/', menu, name='menu'),
    path('menu/<slug:category_slug>/', category_menu, name='category_menu'),
    path('cart/', cart_detail, name='cart'),
    path('orders/', orders, name='orders'),
    path('delivery/', delivery, name='delivery'),
    path('contacts/', contacts, name='contacts'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('removeq/<int:product_id>/', remove_quantity, name='remove_quantity'),
    path('create_order/', create_order, name='create_order'),
]