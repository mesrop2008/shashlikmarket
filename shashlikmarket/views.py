from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import get_cart, save_cart
from .forms import OrderForm
from django.contrib import messages

def home(request):
    return render(request, 'index.html')


def menu(request):
    products = Products.objects.order_by('id')
    active_category = 'all'
    context = {'products': products,
    'active_category': active_category}
    return render(request, 'menu.html', context)

def shashlik(request):
    shashliks = Products.objects.filter(category__exact = 'meat')
    active_category = 'meat'
    context = {'shashliks': shashliks,
    'active_category': active_category}
    return render(request, 'menu/shashlik.html', context)

def kebab(request):
    kebab = Products.objects.filter(category__exact = 'kebab')
    active_category = 'kebab'
    context = {'kebabs': kebab,
    'active_category': active_category}
    return render(request, 'menu/kebab.html', context)

def sets(request):
    sets = Products.objects.filter(category__exact = 'set')
    active_category = 'sets'
    context = {'sets': sets,
    'active_category': active_category}
    return render(request, 'menu/set.html', context)

def garnir(request):
    garnir = Products.objects.filter(category__exact = 'garnish')
    active_category = 'garnirs'
    context = {'garnirs': garnir,
    'active_category': active_category}
    return render(request, 'menu/garnir.html', context)

def fish(request):
    fish = Products.objects.filter(category__exact = 'fish')
    active_category = 'fishes'
    context = {'fishes': fish,
    'active_category': active_category}
    return render(request, 'menu/fish.html', context)

def drinks(request):
    drinks = Products.objects.filter(category__exact = 'drinks')
    active_category = 'drinks'
    context = {'drinks': drinks,
    'active_category': active_category}
    return render(request, 'menu/drinks.html', context)

def souces(request):
    souces = Products.objects.filter(category__exact = 'sauce')
    active_category = 'souces'
    context = {'souces': souces,
    'active_category': active_category}
    return render(request, 'menu/souces.html', context)


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
        form = OrderForm
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

#создание заказа
def create_order(request):
    cart = get_cart(request)
      
    total_price = 0
    cart_items = []

    for product_id, item_data in cart.items():
        try:
            product = Products.objects.get(id=product_id)
            item_total = product.price * item_data['quantity']
            total_price += item_total  

           
            cart_items.append({
                'product': product,  # автоматически берет id
                'quantity': item_data['quantity'],
                'total': item_total,
            })
            
        except Products.DoesNotExist:
            continue
   
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
            customer_name = form.cleaned_data['customer_name'],      
            customer_phone = form.cleaned_data['customer_phone'],    
            delivery_type = form.cleaned_data['delivery_type'],     
            customer_address = form.cleaned_data['customer_address'],
            pay_type=form.cleaned_data['pay_type'],                
            total_price=total_price
            )
                        
            for product_id, item_data in cart.items():
                try:
                    product = Products.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order = order,       
                        product = product,    
                        quantity = item_data['quantity']  
                    )
                except Products.DoesNotExist:
                    continue
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
        'total_price': total_price 
    }
            
    return render(request, 'orders/create_order.html', context)

def orders(request):
    order_ids = request.session.get('user_orders', [])
    
    orders = Order.objects.filter(id__in=order_ids)\
                         .prefetch_related('items__product')\
                         .order_by('-created_at')
    active_order_ids = []
    orders_data = []
    for order in orders:
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
        'orders': orders_data,
    }
    return render(request, 'order.html', context)

def delivery(request):
    return render(request, 'delivery.html')

def contacts(request):
    return render(request, 'contacts.html')



