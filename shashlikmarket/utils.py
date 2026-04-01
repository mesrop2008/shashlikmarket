from .models import Products
from shashlikmarket.types.cart_types import *

def get_cart(request) -> dict[str, CartItem]:
    raw = request.session.get("cart", {})
    cart: dict[str, CartItem] = {}

    for product_id, item in raw.items():
        if isinstance(item, CartItem):
            cart[product_id] = item
        else:
            cart[product_id] = CartItem.from_dict(item)
    return cart

def clean_cart(request):
    cart = get_cart(request)

    if not cart:
        return cart

    product_ids = list(cart.keys())
    valid_ids = {
        str(product_id) for product_id in Products.objects.filter(id__in=product_ids).values_list("id", flat=True)
    }

    cleaned_cart = {product_id: item for product_id, item in cart.items() if product_id in valid_ids}

    if len(cleaned_cart) != len(cart):
          save_cart(request, cleaned_cart)

    return cleaned_cart

#save cart in session
def save_cart(request, cart: dict[str, CartItem]):
    request.session['cart'] = {product_id: item.to_dict() for product_id, item in cart.items()}
    request.session.modified = True