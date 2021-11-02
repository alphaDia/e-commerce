from django.shortcuts import render
from store.models import Product

def home(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        
    print(request.session.session_key)
    products = Product.objects.filter(is_available=True)
    context = {'products': products}
    return render(request, 'home.html', context)
