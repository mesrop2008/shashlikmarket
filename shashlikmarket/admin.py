from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Products
import math

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_with_currency', 'category', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Нет изображения"
    preview.short_description = "Превью"
    def price_with_currency(self, obj):
        if obj.price % 1 == 0:
            return f"{int(obj.price)} ₽"
        return f"{obj.price:.2f} ₽"
    price_with_currency.short_description = "Цена"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = ['product', 'quantity', 'get_price']
    
    def get_price(self, obj):
        return f"{obj.product.price} ₽"
    get_price.short_description = "Цена за шт."
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'customer_name', 
        'customer_phone', 
        'get_delivery_type', 
        'get_status', 
        'total_price', 
        'created_at',
        'quick_actions' 
    ]
    
    list_filter = [
        'status',
        'delivery_type', 
        'pay_type',
        'created_at'
    ]
    
    search_fields = [
        'customer_name',
        'customer_phone', 
        'id'
    ]
    
    readonly_fields = [
        'id',
        'customer_name',
        'customer_phone', 
        'delivery_type',
        'customer_address',
        'pay_type',
        'total_price',
        'created_at',
        'get_items_display'
    ]
    
    inlines = [OrderItemInline]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_status(self, obj):
        """Показывает статус с цветом"""
        colors = {
            'pending': 'orange',
            'preparing': 'blue', 
            'ready': 'green',
            'completed': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status.short_description = "Статус"
    
    def get_delivery_type(self, obj):
        return obj.get_delivery_type_display()
    get_delivery_type.short_description = "Способ получения"
    
    def get_items_display(self, obj):
        items = []
        for item in obj.items.all():
            items.append(f"{item.quantity} × {item.product.name} - {item.product.price} ₽")
        return format_html("<br>".join(items))
    get_items_display.short_description = "Состав заказа"
    
    def quick_actions(self, obj): 
        """Кнопки для быстрой смены статуса"""
        if obj.status == 'pending':
            return format_html('<span style="color: gray;">В обработке</span>')
        elif obj.status == 'preparing':
            return format_html('<span style="color: blue;">Готовится</span>')
        elif obj.status == 'ready':
            return format_html('<span style="color: green;">✅ Готов к выдаче</span>')
        else:
            return format_html('<span style="color: gray;">✅ Завершен</span>')
    quick_actions.short_description = "Текущий статус"  

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'id', 
                'customer_name', 
                'customer_phone', 
                'get_items_display',
                'total_price',
                'created_at'
            )
        }),
        ('Детали заказа', {
            'fields': (
                'delivery_type',
                'customer_address', 
                'pay_type',
                'status'  
            )
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_filter = ['order__status']
    readonly_fields = ['order', 'product', 'quantity']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False