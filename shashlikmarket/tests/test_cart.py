import pytest
from django.test import RequestFactory
from shashlikmarket.utils import get_cart, save_cart

class DummySession(dict):
    """A simple dict-based mock of Django session with a 'modified' attribute for testing."""
    def __init__(self):
        super().__init__()
        self.modified = False

@pytest.fixture
def request_with_session():
    factory = RequestFactory()
    request = factory.get("/")
    request.session = DummySession()
    return request

class TestCartsUtilities:
    def test_get_empty_cart(self, request_with_session):
        cart = get_cart(request_with_session)
        assert cart == {}

    def test_save_cart(self, request_with_session):
        cart_data = {'1': {'quantity': 2, 'name': 'Test', 'price': '100'}}
        save_cart(request_with_session, cart_data)
        retrieved_cart = get_cart(request_with_session)
        assert retrieved_cart == cart_data
