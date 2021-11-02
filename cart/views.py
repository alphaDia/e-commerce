from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from cart.models import Cart, CartItem


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

    try:
        cart_item = CartItem.objects.get(
            product=product, cart=_create_cart(request))
       
        
        cart_item.quantity += 1
        cart_item.save()
      
        return cart_item
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            quantity=1, product=product, cart=_create_cart(request))
     
        return cart_item

# views starts here
def add_cart_item(request, product_id):
    _add_product_to_cart(request, product_id)
    return redirect('cart')

def remove_cart_item(request, product_id):
    CartItem.objects.get(product__id=product_id, cart__cart_id=_cart_id(request)).delete()
    return redirect('cart')

def remove_product_from_cart(request, product_id):
    cart_item = CartItem.objects.get(product__id=product_id, cart__cart_id=_cart_id(request))
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else: cart_item.delete()
    
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
