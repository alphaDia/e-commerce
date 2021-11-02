from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product
from category.models import Category



def store(request):
    products = Product.objects.filter(is_available=True)
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = products.count()
    
    context  = {
        'products': paged_products, 
        'count': count,
        'label': 'Our Store'
    }
    
    return render(request, 'store/store.html', context)

def sort_by_category(request, category_slug):
    products = Product.objects.filter(is_available=True, category__slug=category_slug)
    count    = products.count()
    
    context  = {'products': products, 'count': count,  'label': 'Our Store'}
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
       product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
       context = {'product': product}
           
       return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET and request.GET['keyword'] != '':
        keyword = request.GET['keyword']
        products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
        context = {
            'products': products,
            'count': products.count(),
            'label': f'Results for {keyword}'
        }
        
        return render(request, 'store/store.html', context)
    return render(request, 'store/store.html')
        