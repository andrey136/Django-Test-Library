from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_view(request, *args, **kwargs):
    print(request, args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello World!</h1>")
    return render(request, "home.html", {})

def products_view(request, *args, **kwargs):
    my_context = {
        "fruits":{
            0: "apple",
            1: "orange",
            2: "mango",
            3: "kiwi"
        }
    }

    return render(request, 'products.html', my_context)

def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about us",
        "this_is_true": True,
        "my_number": 123,
        "my_list": [12, 4245, 312, 'kds']
    }
    return render(request, 'about.html', my_context)

def shoplist_view(request, *args, **kwargs):
    my_context = {
        "title": "animals",
        "kittens":["JB","Jess","Coco","Rafael"],
        "my_html": "<h1>Hello World</h1>"
    }
    return render(request, 'shopList.html', my_context)