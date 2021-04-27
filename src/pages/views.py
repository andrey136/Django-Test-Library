from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_view(request, *args, **kwargs):
    print(request, args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello World!</h1>")
    return render(request, "home.html", {})

def products_view(request, *args, **kwargs):
    return render(request, 'products.html', {})

def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about us",
        "my_number": 123,
        "my_list": [12, 532, 1137]
    }
    return render(request, 'about.html', my_context)