import pytest
from django.test import RequestFactory
from shashlikmarket.views import menu, category_menu
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
        


