from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import *
from .utils import get_cart, save_cart, clean_cart
from .forms import OrderForm


def home(request):
    return render(request, 'index.html')


def menu(request):
    cart = clean_cart(request)
    products = Products.objects.order_by('id')
    active_category = 'all'
    
    for p in products:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)
            
    context = {
        'products': products,
        'active_category': active_category,
        'cart': cart,  
    }
    return render(request, 'menu.html', context)


def shashlik(request):
    cart = get_cart(request)
    shashliks = Products.objects.filter(category__exact='meat')
    active_category = 'meat'
        
    for p in shashliks:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'shashliks': shashliks,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/shashlik.html', context)


def kebab(request):
    cart = get_cart(request)
    kebabs = Products.objects.filter(category__exact='kebab')
    active_category = 'kebab'
    
    for p in kebabs:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'kebabs': kebabs,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/kebab.html', context)


def sets(request):
    cart = get_cart(request)
    sets_qs = Products.objects.filter(category__exact='set')
    active_category = 'sets'
        
    for p in sets_qs:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'sets': sets_qs,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/set.html', context)


def garnir(request):
    cart = get_cart(request)
    garnirs = Products.objects.filter(category__exact='garnish')
    active_category = 'garnirs'
        
    for p in garnirs:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'garnirs': garnirs,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/garnir.html', context)


def fish(request):
    cart = get_cart(request)
    fishes = Products.objects.filter(category__exact='fish')
    active_category = 'fishes'
    
    for p in fishes:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'fishes': fishes,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/fish.html', context)


def drinks(request):
    cart = get_cart(request)
    drinks_qs = Products.objects.filter(category__exact='drinks')
    active_category = 'drinks'
       
    for p in drinks_qs:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'drinks': drinks_qs,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/drinks.html', context)


def souces(request):
    cart = get_cart(request)
    souces_qs = Products.objects.filter(category__exact='sauce')
    active_category = 'souces'
        
    for p in souces_qs:
        p.quantity = cart.get(str(p.id), {}).get('quantity', 0)

    context = {
        'souces': souces_qs,
        'active_category': active_category,
        'cart': cart
    }
    return render(request, 'menu/souces.html', context)


@require_GET
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = get_cart(request)
    
    image_url = product.image.url if product.image else ''

    if str(product.id) not in cart:
        cart[str(product.id)] = {
            'quantity': 1,
            'name': product.name,
            'imagepath': image_url,
            'price': str(product.price),
        }
    else:
        cart[str(product.id)]['quantity'] += 1
    
    save_cart(request, cart)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_quantity = sum(item['quantity'] for item in cart.values())
        cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} добавлен в корзину',
            'cart_total_quantity': total_quantity,
            'product_quantity': cart[str(product.id)]['quantity'],
            'product_id': product_id,
            'cart_total': cart_total
        })
    
    return redirect('cart')


@require_GET
def remove_quantity(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)  
    
    if product_id_str in cart:
        if cart[product_id_str]["quantity"] > 1:
            cart[product_id_str]["quantity"] -= 1
        else:
            del cart[product_id_str]
            
    save_cart(request, cart)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_quantity = sum(item['quantity'] for item in cart.values())
        product_quantity = cart.get(product_id_str, {}).get('quantity', 0)
        cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'cart_total_quantity': total_quantity,
            'product_quantity': product_quantity,
            'product_id': product_id,
            'cart_total': cart_total
        })
    
    return redirect('cart')


@require_GET
def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)  
    product_name = ""
    
    if product_id_str in cart:
        product_name = cart[product_id_str]['name']
        del cart[product_id_str]
        save_cart(request, cart)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total_quantity = sum(item['quantity'] for item in cart.values())
        cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'cart_total_quantity': total_quantity,
            'product_id': product_id,
            'cart_total': cart_total,
            'message': f'{product_name} удален из корзины'
        })
    
    return redirect('cart')


def cart_detail(request):
    cart = clean_cart(request)
    items = []
    total = 0

    product_ids = list(cart.keys())
    products_list = Products.objects.filter(id__in=product_ids)
    products_dict = {str(p.id): p for p in products_list}

    updated_cart = cart.copy()

    for product_id, item in cart.items():
        product = products_dict.get(str(product_id))  
        if not product:
            continue

        quantity = item.get('quantity', 0)
        price = float(product.price)
        subtotal = quantity * price
        total += subtotal

        items.append({
            'product': product,
            'name': product.name,
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'imagepath': item.get('imagepath')
        })
    
    request.session['cart'] = updated_cart
    request.session.modified = True
   
    context = {
        'items': items,
        'total': total,
    }

    return render(request, 'cart.html', context)


def create_order(request):
    cart = get_cart(request)
    total_price = 0
    cart_items = []

    product_ids = list(cart.keys())
    products_list = Products.objects.filter(id__in=product_ids)
    products_dict = {str(p.id): p for p in products_list}

    for product_id, item_data in cart.items():
        product = products_dict.get(str(product_id))
        if not product:
            continue

        quantity = item_data.get('quantity', 0)
        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
            'imagepath': item_data.get('imagepath')
        })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                customer_phone=form.cleaned_data['customer_phone'],
                delivery_type=form.cleaned_data['delivery_type'],
                customer_address=form.cleaned_data['customer_address'],
                pay_type=form.cleaned_data['pay_type'],
                total_price=total_price
            )

            for product_id, item_data in cart.items():
                product = products_dict.get(str(product_id))
                if product:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data.get('quantity', 0)
                    )

            if 'user_orders' not in request.session:
                request.session['user_orders'] = []

            request.session['user_orders'].append(order.id)
            request.session.modified = True

            save_cart(request, {})
            return redirect('orders')
    else:
        form = OrderForm()
   
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'orders/create_order.html', context)


def orders(request):
    cart = get_cart(request)
    order_ids = request.session.get('user_orders', [])
    
    orders_qs = Order.objects.filter(id__in=order_ids)\
                             .prefetch_related('items__product')\
                             .order_by('-created_at')
    active_order_ids = []
    orders_data = []
    
    for order in orders_qs:
        if order.status != 'completed':
            active_order_ids.append(order.id)
            
            order_data = {
                'id': order.id,
                'customer_name': order.customer_name,
                'customer_phone': order.customer_phone,
                'delivery_type': order.get_delivery_type_display(),
                'customer_address': order.customer_address,
                'pay_type': order.get_pay_type_display(),
                'status': order.status,
                'status_display': order.get_status_display(),
                'created_at': order.created_at.strftime('%d.%m.%Y в %H:%M'),
                'total_price': order.total_price,
                'items': order.items.all()  
            }
            orders_data.append(order_data)
        
    
    request.session['user_orders'] = active_order_ids
    request.session.modified = True
    
    context = {
        'orders': orders_data
    }
    return render(request, 'order.html', context)


def delivery(request):
    return render(request, 'delivery.html')


def contacts(request):
    return render(request, 'contacts.html')
