from django.shortcuts import render, get_object_or_404
from products.models import Product
from products.forms import ProductForm

# Create your views here.

def home_view(request):
    print('HOME VIEW')
    return render(request, 'home_view.html', {})

def products_list_view(request):
    objs = Product.objects.all()
    context = {
        "products": objs
    }
    return render(request, 'products/products_list.html', context)

def products_detail_view(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {
        "product": obj
    }
    return render(request, 'products/products_detail.html', context)

def products_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()
    context = {
        "form": ProductForm
    }
    return render('create/', 'products/products_create.html', context)