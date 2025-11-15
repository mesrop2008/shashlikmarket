import pytest
from django.test import RequestFactory
from shashlikmarket.views import menu
from shashlikmarket.models import Products
from shashlikmarket.utils import clean_cart
from decimal import Decimal
from django.test import Client
from django.urls import reverse

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



