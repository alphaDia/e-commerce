from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.
def store(request):
    products = Product.objects.filter(is_available=True)
    count    = products.count()
    
    context  = {
        'products': products, 
        'count': count
    }
    
    return render(request, 'store/store.html', context)

def sort_by_category(request, category_slug):
    products = Product.objects.filter(is_available=True, category__slug=category_slug)
    count    = products.count()
    
    context  = {'products': products, 'count': count}
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
       product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
       context = {'product': product}
           
       return render(request, 'store/product_detail.html', context)