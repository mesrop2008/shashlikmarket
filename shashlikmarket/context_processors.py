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
    cart_total_quantity = sum(item.quantity for item in cart.values() if item.quantity is not None)

    return {
        'cart_total_quantity': cart_total_quantity
    }