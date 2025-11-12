"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shashlikmarket.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('menu/', menu, name='menu'),
     path('menu/shashlik/', category_menu, {'category_slug': 'shashlik'}, name='shashlik'),
    path('menu/kebab/', category_menu, {'category_slug': 'kebab'}, name='kebab'),
    path('menu/sets/', category_menu, {'category_slug': 'sets'}, name='sets'),
    path('menu/garnir/', category_menu, {'category_slug': 'garnir'}, name='garnir'),
    path('menu/fish/', category_menu, {'category_slug': 'fish'}, name='fish'),
    path('menu/drinks/', category_menu, {'category_slug': 'drinks'}, name='drinks'),
     path('menu/souces/', category_menu, {'category_slug': 'souces'}, name='souces'),
    path('cart/', cart_detail, name='cart'),
    path('orders/', orders, name='orders'),
    path('delivery/', delivery, name='delivery'),
    path('contacts/', contacts, name='contacts'),
    path('add/<int:product_id>/', add_to_cart, name = 'add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name = 'remove_from_cart'),
    path('removeq/<int:product_id>/', remove_quantity, name = 'remove_quantity'),
    path('create_order/', create_order, name='create_order'),

    

]
