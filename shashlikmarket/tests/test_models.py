import pytest
from decimal import Decimal
from shashlikmarket.models import Products, Order, OrderItem

@pytest.mark.django_db
class TestProductsModel:
    def test_product_string_representation(self):
        product = Products.objects.create(
            name="Шашлык из свинины",
            price=Decimal("350.00"),
            category="meat"
        )
        assert str(product) == "Шашлык из свинины"
    
    def test_product_creation(self):
        product = Products.objects.create(
            name = "Кебаб",
            description = "Вкусный кебаб",
            weight = 200.0,
            price = Decimal("350.00"),
            category = "Meat"
        )
        assert product.id is not None
        assert product.price == Decimal("350")

@pytest.mark.django_db
class TestOrderModel:
    def test_order_creation(self):
        order = Order.objects.create(
            customer_name =  "Иван Иванов",
            customer_phone = "89500903533",
            delivery_type = "delivery",
            customer_address = "ул. Пискунова 40",
            pay_type = "cash",
            total_price = Decimal("500.00")
        )
        assert order.status == "pending"
        assert str(order) == f"Заказ #{order.id} - Иван Иванов"

