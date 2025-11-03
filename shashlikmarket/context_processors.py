
from shashlikmarket.utils import get_cart

def menu_urls(request):
    return {
        'menu_urls': [
            'menu', 'shashlik', 'kebab', 'sets', 
            'garnirs', 'fishes', 'drinks', 'souces'
        ]
    }

def cart_context(request):
    cart = get_cart(request)
    cart_items_count = sum(item['quantity'] for item in cart.values())
    return {
        'cart_items_count': cart_items_count,
        'cart_total': cart_items_count  
    }