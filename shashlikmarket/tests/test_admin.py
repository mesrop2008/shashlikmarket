import pytest
from django.contrib.admin.sites import AdminSite
from shashlikmarket.admin import OrderAdmin, ProductAdmin, OrderItemAdmin
from shashlikmarket.models import Order, Products, OrderItem

@pytest.mark.django_db
def test_order_admin_list_display():
    site = AdminSite()
    admin = OrderAdmin(Order, site)
    assert 'customer_name' in admin.list_display
    assert 'quick_actions' in admin.list_display

@pytest.mark.django_db
def test_product_preview_and_price():
    site = AdminSite()
    admin = ProductAdmin(Products, site)
    product = Products.objects.create(name="Тест", price=250)
    assert admin.price_with_currency(product) == "250 ₽"
    assert admin.preview(product) == "Нет изображения"

@pytest.mark.django_db
def test_order_item_admin_permissions():
    site = AdminSite()
    admin = OrderItemAdmin(OrderItem, site)
    request = None
    assert admin.has_add_permission(request) is False
    assert admin.has_delete_permission(request) is False