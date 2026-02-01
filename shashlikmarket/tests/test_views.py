import pytest
from django.test import RequestFactory
from shashlikmarket.views import menu, category_menu, create_order, orders
from shashlikmarket.models import Products, OrderItem, Order
from shashlikmarket.utils import clean_cart
from decimal import Decimal
from django.test import Client
from django.urls import reverse
from django.http import QueryDict

class DummySession(dict):
    """A simple dict-based mock of Django session with a 'modified' attribute for testing."""
    def __init__(self):
        super().__init__()
        self.modified = False

@pytest.fixture
def request_with_session():
    factory = RequestFactory()
    request = factory.get("/menu/")
    request.session = DummySession()
    return request

@pytest.mark.django_db
def test_menu_view_shows_products(request_with_session):
    p1 = Products.objects.create(name="Шашлык", price=Decimal("250"), weight=100)
    p2 = Products.objects.create(name="Кебаб", price=Decimal("150"), weight=50)

    client = Client()
    session = client.session
    session['cart'] = { str(p1.id): {"quantity": 2} }
    session.save()

    response = client.get(reverse("menu"))

    assert response.status_code == 200
    context = response.context

    assert "products" in context
    assert "cart" in context
    assert context["active_category"] == "all"

    products = context["products"]
    assert len(products) == 2

    product1 = next(p for p in products if p.id == p1.id)
    product2 = next(p for p in products if p.id == p2.id)

    assert product1.quantity == 2
    assert product2.quantity == 0
    
@pytest.mark.django_db
class TestShowCategories:
    @pytest.mark.parametrize(
        "category_slug,db_filter,template_var,active_category",
        [
            ("shashlik", "meat",   "shashliks", "meat"),
            ("kebab",    "kebab",  "kebabs",    "kebab"),
            ("sets",     "set",    "sets",      "sets"),
            ("garnir",   "garnish","garnirs",   "garnirs"),
            ("fish",     "fish",   "fishes",    "fishes"),
            ("drinks",   "drinks", "drinks",    "drinks"),
            ("sauces",   "sauce",  "sauces",    "sauces"),
        ]
    )
    def test_category_menu_each_category(request_with_session, category_slug, db_filter, template_var, active_category):
        client = Client()

        p1 = Products.objects.create(name="A", price=Decimal("100"), weight=100, category=db_filter)
        p2 = Products.objects.create(name="B", price=Decimal("100"), weight=100, category=db_filter)
        Products.objects.create(name="C", price=Decimal("100"), weight=100, category="OTHER")

        session = client.session
        session["cart"] = {str(p1.id): {"quantity": 3}}
        session.save()

        url = reverse("category_menu", args=[category_slug])
        response = client.get(url)

        assert response.status_code == 200
        context = response.context

        products = context[template_var]
        assert len(products) == 2

        product1 = next(p for p in products if p.id == p1.id)
        product2 = next(p for p in products if p.id == p2.id)

        assert product1.quantity == 3
        assert product2.quantity == 0
        assert all(p.category == db_filter for p in products)

        assert context["active_category"] == active_category

        Products.objects.all().delete()
    def test_category_menu_invalid_slug_calls_menu(self, request_with_session, mocker):
        '''We check that if the slug is incorrect, the normal menu is called'''
        mock_menu = mocker.patch('shashlikmarket.views.menu', return_value='menu called')
        request = request_with_session

        result = category_menu(request, category_slug='invalid')
        assert result == 'menu called'
    
    def test_category_menu_no_slug_calls_menu(self, request_with_session, mocker):
        '''We check that if there is no slug, the normal menu is called'''
        mock_menu = mocker.patch('shashlikmarket.views.menu', return_value='menu called')
        request = request_with_session

        result = category_menu(request, category_slug='None')
        assert result == 'menu called'
        
class TestCreateOrder:
    @pytest.mark.django_db
    def test_create_order_get_render_form(self, request_with_session):
        product = Products.objects.create(name="Шашлык", price=Decimal("250"), weight=150)
        request = request_with_session
        request.session["cart"] = {str(product.id): {"quantity": 2, "name": product.name, "price": str(product.price)}}
        request.method = "GET"

        response = create_order(request)
        assert response.status_code == 200
        assert hasattr(response, "content")

    @pytest.mark.django_db
    def test_create_order_post_creates_order(self, request_with_session):
        product = Products.objects.create(name="Шашлык", price=Decimal("250"), weight=150)
        request = request_with_session
        request.session["cart"] = {str(product.id): {"quantity": 2, "name": product.name, "price": str(product.price)}}
        request.method = "POST"

        post = QueryDict('', mutable=True)
        post.update({
            'customer_name': 'Иван',
            'customer_phone': '+79500903533',
            'delivery_type': 'delivery',
            'customer_address': 'ул. Пушкина, д.1',
            'pay_type': 'cash'
        })
        request.POST = post

        response = create_order(request)
        assert response.status_code == 302

        order = Order.objects.first()
        assert order is not None
        assert order.customer_name == 'Иван'
        assert order.customer_phone == '+79500903533'
        assert order.total_price == product.price * 2

        item = OrderItem.objects.first()
        assert item is not None
        assert item.product == product
        assert item.quantity == 2
        assert request.session["cart"] == {}
        assert order.id in request.session["user_orders"]

@pytest.mark.django_db
def test_orders_view_shows_only_active_orders():
    client = Client()
    order1 = Order.objects.create(
        customer_name="Иван",
        customer_phone="89500903533",
        delivery_type="delivery",
        customer_address="ул. Пушкина, д.1",
        pay_type="cash",
        total_price=500,
        status="pending"
    )
    order2 = Order.objects.create(
        customer_name="Петр",
        customer_phone="89086508038",
        delivery_type="pickup",
        customer_address="ул. Лермонтова, д.2",
        pay_type="card",
        total_price=300,
        status="completed"
    )

    product = Products.objects.create(name="Шашлык", price=Decimal("250"), weight=100)
    OrderItem.objects.create(order=order1, product=product, quantity=2)
    OrderItem.objects.create(order=order2, product=product, quantity=1)

    session = client.session
    session['user_orders'] = [order1.id, order2.id]
    session.save()

    response = client.get('/orders/')  
    assert response.status_code == 200
    orders_in_context = response.context['orders']

    assert len(orders_in_context) == 1
    assert orders_in_context[0]['id'] == order1.id
    assert orders_in_context[0]['status'] == "pending"