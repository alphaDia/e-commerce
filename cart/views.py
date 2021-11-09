from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from store.models import Product, Variation
from cart.models import Cart, CartItem


def get_query(request, size=None, color=None):
    if request.method == 'POST':
        size = request.POST.get('size')
        color = request.POST.get('color')
        
    if request.method == 'GET':
        size = request.GET.get('size')
        color = request.GET.get('color')

    if size==None  or color==None:
        raise Http404("S'il vous plait veillez indique une couleur et une taille")
    
    return color, size

# create a session if the existing one is already epired


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# create a cart based on session key


def _create_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        return cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        return cart


def _add_product_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)    
    color, size = get_query(request)

    try:
        cart_item = CartItem.objects.get(
            product=product, product_color=color, product_size=size, cart=_create_cart(request))

        cart_item.quantity += 1
        cart_item.save()

        return cart_item
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            quantity=1, product_color=color, product_size=size, product=product, cart=_create_cart(request))

        return cart_item

# views starts here


def add_cart_item(request, product_id):
    _add_product_to_cart(request, product_id)
    return redirect('cart')


def remove_cart_item(request, product_id):
    color, size = get_query(request)
    CartItem.objects.get(product__id=product_id,
                         product_color=color, product_size=size,
                         cart__cart_id=_cart_id(request)).delete()
    return redirect('cart')


def remove_product_from_cart(request, product_id):
    color, size = get_query(request)
    cart_item = CartItem.objects.get(
        product__id=product_id, product_color=color, product_size=size, cart__cart_id=_cart_id(request))

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    tax = 0
    try:
        cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = tax * total
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, 'cart/cart.html', context)
