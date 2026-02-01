import pytest
from django.test import RequestFactory
from shashlikmarket.utils import get_cart, save_cart
from shashlikmarket.models import Products
from shashlikmarket.views import add_to_cart, remove_quantity, remove_from_cart
from decimal import Decimal

class DummySession(dict):
    """Mock Django session with 'modified' attribute."""
    def __init__(self):
        super().__init__()
        self.modified = False

@pytest.fixture
def request_with_session():
    factory = RequestFactory()
    request = factory.get("/")
    request.session = DummySession()
    return request

@pytest.mark.django_db
class TestCartsUtilities:
    def test_get_empty_cart(self, request_with_session):
        cart = get_cart(request_with_session)
        assert cart == {}

    def test_save_cart(self, request_with_session):
        cart_data = {'1': {'quantity': 2, 'name': 'Test', 'price': '100'}}
        save_cart(request_with_session, cart_data)
        retrieved_cart = get_cart(request_with_session)
        assert retrieved_cart == cart_data

    def test_add_to_cart_new_item(self, request_with_session):
        product = Products.objects.create(
            name="Шашлык",
            price=Decimal("250"),
            weight=150
        )
        request = request_with_session

        response = add_to_cart(request, product.id)
        cart = request.session.get("cart", {})

        assert response.status_code == 302
        assert str(product.id) in cart
        assert cart[str(product.id)]["quantity"] == 1
        assert cart[str(product.id)]["name"] == product.name
        assert Decimal(cart[str(product.id)]["price"]) == product.price
       
    def test_add_to_cart_increases_quantity(self, request_with_session):
            product = Products.objects.create(
                name="Шашлык",
                price=Decimal("250"),
                weight=150
            )
            request = request_with_session
            add_to_cart(request, product.id)
            add_to_cart(request, product.id)
            cart = request.session.get("cart", {})

            assert cart[str(product.id)]["quantity"] == 2

    def test_remove_quantity_decreases_quantity(self, request_with_session):
        product = Products.objects.create(
                name="Шашлык",
                price=Decimal("250"),
                weight=150
            )
        
        request = request_with_session
        add_to_cart(request, product.id)
        add_to_cart(request, product.id)

        remove_quantity(request, product.id)
        cart = request.session.get("cart", {})
        
        assert cart[str(product.id)]["quantity"] == 1
    
    def test_remove_quantity_claers_item(self, request_with_session):
        '''If there is one item in the basket, it should be removed.'''
        product = Products.objects.create(
        name="Шашлык",
        price=Decimal("250"),
        weight=150
        )
        
        request = request_with_session
        add_to_cart(request, product.id)

        remove_quantity(request, product.id)
        cart = request.session.get("cart", {})

        assert cart == {}
    
    def remove_from_cart_clears_items(self, request_with_session):
        product = Products.objects.create(
                name="Шашлык",
                price=Decimal("250"),
                weight=150
            )
        
        request = request_with_session
        add_to_cart(request, product.id)
        add_to_cart(request, product.id)

        remove_from_cart(request, product.id)
        cart = request.session.get("cart", {})

        assert cart == {}

            
    
    