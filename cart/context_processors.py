from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem


def product_count(request):
    product_number = 0
    key = request.session.session_key
    
    try:
        cart = Cart.objects.get(cart_id=key)
        product_number = CartItem.objects.filter(cart=cart).count()
    except ObjectDoesNotExist:
        pass
    
    
    return dict(product_number=product_number)