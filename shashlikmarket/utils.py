#get cart
from .models import Products
def get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def clean_cart(request):
    cart = get_cart(request)

    if not cart:
        return cart

    product_ids = list(cart.keys())
    valid_ids = set(
        str(id) for id in
        Products.objects.filter(id__in=product_ids).values_list('id', flat=True)
    )

    cleaned_cart = {
          pid: item for pid, item in cart.items()
          if pid in valid_ids
      }

    if len(cleaned_cart) != len(cart):
          save_cart(request, cleaned_cart)

    return cleaned_cart

#save cart in session
def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True