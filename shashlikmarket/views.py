from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import get_cart, save_cart

def home(request):
    return render(request, 'index.html')

def menu(request):
    products = Products.objects.order_by('id')
    active_category = 'all'
    context = {'products': products}
    return render(request, 'menu.html', context, {'active_category': active_category})

def shashlik(request):
    shashliks = Products.objects.filter(category__exact = 'meat')
    active_category = 'meat'
    context = {'shashliks': shashliks}
    return render(request, 'menu/shashlik.html', context, {'active_category': active_category})

def kebab(request):
    kebab = Products.objects.filter(category__exact = 'kebab')
    active_category = 'kebab'
    context = {'kebabs': kebab}
    return render(request, 'menu/kebab.html', context, {'active_category': active_category})

def sets(request):
    sets = Products.objects.filter(category__exact = 'set')
    active_category = 'sets'
    context = {'sets': sets}
    return render(request, 'menu/set.html', context, {'active_category': active_category})

def garnir(request):
    garnir = Products.objects.filter(category__exact = 'garnish')
    active_category = 'garnirs'
    context = {'garnirs': garnir}
    return render(request, 'menu/garnir.html', context, {'active_category': active_category})

def fish(request):
    fish = Products.objects.filter(category__exact = 'fish')
    active_category = 'fishes'
    context = {'fishes': fish}
    return render(request, 'menu/fish.html', context, {'active_category': active_category})

def drinks(request):
    drinks = Products.objects.filter(category__exact = 'drinks')
    active_category = 'drinks'
    context = {'drinks': drinks}
    return render(request, 'menu/drinks.html', context, {'active_category': active_category})

def souces(request):
    souces = Products.objects.filter(category__exact = 'sauce')
    active_category = 'souces'
    context = {'souces': souces}
    return render(request, 'menu/souces.html', context, {'active_category': active_category})


#добавление
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_cart(request)

    if str(product.id) not in cart:
        cart[str(product_id)] = {
            'quantity': 1,
            'name': product.name,
            'imagepath': product.imagepath,
            'price': str(product.price),
            
        }
    else:
        cart[str(product.id)]['quantity'] += 1

    save_cart(request, cart)
    return redirect('cart')

#удаление
def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)  
    del cart[product_id_str]

    save_cart(request, cart)
    return redirect('cart')  

def remove_quantity(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)  
    
    if product_id_str in cart:
        if cart[product_id_str]["quantity"] > 1:
            cart[product_id_str]["quantity"] -= 1
        else:
            del cart[product_id_str]
            
    save_cart(request, cart)
    return redirect('cart')


#корзина
def cart_detail(request):
    cart = get_cart(request)
    items = []
    total = 0
    
    for product_id, item in cart.items():
        product = Products.objects.get(id=product_id)
        quantity = item['quantity']
        price = item['price']
        name = item['name']
        subtotal = int(quantity) * int(price)
        total += subtotal
        
        items.append({
            'product': product,
            'name': name,
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'imagepath': item.get('imagepath')
        })

        return render(request, 'cart.html', {'items': items,'total': total})  


def orders(request):
    return render(request, 'order.html')

def delivery(request):
    return render(request, 'delivery.html')

def contacts(request):
    return render(request, 'contacts.html')



