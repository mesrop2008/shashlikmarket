# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from cloudinary.models import CloudinaryField
from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)  
    @property
    def price_display(self):
        if self.price % 1 == 0:
            return f"{int(self.price)} ₽"
        return f"{self.price:.2f} ₽"
    @property
    def weight_display(self):
        if self.weight % 1 == 0:
            return f"{int(self.weight)}г"
        return f"{self.weight:.2f}г"
            
    class Meta:
        db_table = 'products'
        managed = False  # можно оставить False, если таблица уже есть
        indexes = [
            models.Index(fields=['category'], name='idx_product_category'),
        ]
    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('preparing', 'Готовится'), 
        ('ready', 'Готов'),
        ('completed', 'Завершен'),
    ]
    
    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    ]
    
    PAY_CHOICES = [
        ('cash', 'Наличными курьеру'),
        ('card', 'Переводом курьеру')
    ]
    
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    delivery_type = models.CharField(
        max_length=20, 
        choices=DELIVERY_CHOICES, 
        default='delivery',
        verbose_name="Способ получения"
    )
    customer_address = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Адрес доставки"
    )
    pay_type = models.CharField(
        max_length=20, 
        choices=PAY_CHOICES, 
        default='cash',
        verbose_name="Способ оплаты"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Статус заказа"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Общая сумма"
    )
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.customer_name}"
    
    class Meta:
        verbose_name = "Заказ"  # Название в единственном числе
        verbose_name_plural = "Заказы"  # Название во множественном числе
        ordering = ['-created_at']  # Сортировка по умолчанию (новые сверху)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        'Products', 
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"

    