## Virtual Environment

### Creating virtual environment

```
virtualenv -p python3 .

source bin/activate (or .\Scripts\activate)

pip3 install django==2.1.5
```

### Activating virtual environment

```
cd django-project-folder

source bin/activate  (or .\Scripts\activate)

deactivate
```

### Looking at the requirements
```
pip3 freeze
```

Why is it important to use virtual environment for your projects?
* It keeps all the requirements seperate.

### 3 ways to create a virtual environment

1. virtualenv venv
1. virtualenv venv2 -p python3
1. virtualenv venv3 -p python3_path
    * Find the location where python3 is intalled
    * Add the path to the command
### The 4th method to create virtual environment
```
mkdir venv4

cd venv4

virtualenv . -p python3
```

## Django Project

### Starting a New Django Project in a Vitual Environment

```
mkdir src

cd src

django-admin startproject trydjango . 

# trydjango --> name of the project
# .         --> current folder


python manage.py runserver
```
### Running our database
```
python manage.py migrate
```
## Creating an app

### Built-in components

Apps are pieces or components of a bigger django project

In setting.py file in INSTALLED_APPS you put third party apps or your own

### Migrating dbs with projects and creating a super user(admin)
```
python manage.py migrate

python manage.py createsuperuser
```
Then authorize in /admin

### Adding apps
```
python manage.py startapp products

python manage.py startapp cart

python manage.py startapp blog

python manage.py startapp profiles
```
### Creating Models

Code in products/models.py
```
class Product(models.Model):
    title       = models.TextField()
    description = models.TextField()
    price       = models.TextField()
```

Code in products/admin.py
```
from .models import Product

admin.site.register(Product)
```

Add products to the ISTALLED_APPS list in settings.py

Then save the settings.py, models.py and admin.py file

### Migrate commands

As you change models.py save it!!!

ALWAYS run these commands in console after making any changes to models.py
```
python manage.py makemigrations
python manage.py migrate
```
Run in conjuction with each other every single time you make changes to models.py

```
from django.db import models
# Create your models here.
class Product(models.Model):
    title       = models.TextField()
    description = models.TextField()
    price       = models.TextField()
    summary     = models.TextField() --(new line in models.py)
```
## Create Product Objects in the Python shell

### Creating Object
```
 python manage.py shell
 from products.models import Product
 Product.objects.all()
 Product.objects.create()
 Product.objects.create(title='New product 2', description='another one', price='19312', summary='sweet')
```
## New Model Fields
### Starting over

To start over you need to delete all the files in migration folder except for the init.py in products app

Delete sqlite db

Check out https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.AutoField

### Changes in models.py
```
from django.db import models

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=120) # max_length = required
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(decimal_places=2, max_digits=10000)
    summary     = models.TextField()
```
### Further commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser -- because we deleted our sqlite database

python manage.py shell
from products.models import Product
Product.objects.create(title='Newer title', price=239.99, summary='Awesome sause')
```
## Change a model
If blank attribute = False then the field is required to be filled

## Default Homepage to Custom Homepage

First we create a new app "pages" with the following command:

```
python manage.py startapp pages 
```
Then add "pages" to the settings.py INSTALLED_APPS list

Modify pages/views.py file

```
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home_view(request, *args, **kwargs):
    print(request, args, kwargs)
    print(request.user)
    return HttpResponse("<h1>Hello World!</h1>")
```

Modify trydjango/urls.py file

```
from django.contrib import admin
from django.urls import path

from pages.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
]

```

If you want to add another view in the same app, then just create a new function in the same views.py file and import that function from urls.py and add it to the urlpatterns

## Django Templates

The changes in pages/views.py. There is no need for us to write html code in strings. We can use `render` function that has bee imported in views.py by default and that's how we do it.

```
def home_view(request, *args, **kwargs):
    print(request, args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello World!</h1>")
    return render(request, "home.html", {})

```

Then we need to make a new folder called `templates` in the source directory
Create a `home.html` file that will be shown in a browser as an http response.

Also we need to tell django where our templates are.
So go to settings.py, find these lines:
```
from pathlib import Path
from pathlib import PurePath 
# instead of os.path.join() we will use PurePath() 
# which works practically the same way

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

...
...
...

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PurePath(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## Django Templating Engine Basics

Write in templates folder in home.html:
* This is just an example of how django talks to templates
```
<h1>Hello World</h1>
{{ request.user }}
<p>This is a template</p>
```

or 

```
<h1>Hello World</h1>
{{ request.user.is_authenticated }}
<p>This is a template</p>
```

Create base.html. It's where the other templates will take meta data or some common components

Add this code to base.html

```
<!DOCTYPE html>
<html>
<head>
  <title>Coding for entrepreneurs is Doing Try Django</title>
</head>
<body>
    {% block page_content %}
    replace me
    {% endblock %}
</body>
</html>
```

Here {} and %% are just django symbols

block and endblock tell django that inside them the content will be changed

page_content is just a variable

That's what you need to write in home.html:
```
{% extends 'base.html' %}
{% block page_content %}
<h1>Hello World</h1>
<p>This is a template</p>
{% endblock %}
```
extends 'filename' gives us the base file in which you'll put a piece of code
if variable(page_content) is not the same as in the extended file (base.html) then only base.html will be shown

## Including Templates

Create a new file 'nav_bar.html'

Write this code:
```
<nav>
    <ul class="container">
        <li>click 1</li>
        <li>click 2</li>
        <li>click 3</li>
    </ul>
</nav>
```

And then add this piece of code `{% include 'template' %}` change template for the filename where your nav_bar or any other html code was written

## Rendering context in Django

We make a dictionary of the template context that we want to pass and we pass that

In pages/views.py:
```
def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about us",
        "my_number": 123
    }
    return render(request, 'about.html', my_context)
```
My context is a dictionary where we can keep any data that we want to pass to our templates

In templates/about.html
```
{% extends 'base.html' %}

{% block about_page %}
<h1>About page</h1>

<p>

{{ my_text }},
{{ my_number }}

</p>

{% endblock %}
```

We write {{  }}. In them we put the keys of our context(dictionary that we passed in our page/views.py function)

## For Loop in a Template

Write in templates/about.html:

```
{% extends 'base.html' %}

{% block about_page %}
<h1>About page</h1>

<ul>
{% for my_sub_item in my_list %}
<li>{{ forloop.counter }}-{{ my_sub_item }}</li>
{% endfor %}  
</ul>

{% endblock %}
```

* {%%} - as always we put any django code in these;
* my_sub_item - arbitrary name
* in - python operator
* my_list - the key of the context obj we passes to our template from pages/views
* {{ my_sub_item }} - in them we write the arbitrary name we came up with
* {{ forloop.counter }} - return index of the elemnt starting with one

## Using Conditions in a Template

Write in templates/about.html:

```
{% extends 'base.html' %}

{% block about_page %}
<h1>About page</h1>

<ul>
{% for abc in my_list %}

{% if abc == 312 %}
<li>{{ forloop.counter }}-{{ abc|add:22 }}</li>
{% elif abc == "kds" %}
<li>This is not the network</li>
{% else %}
<li>{{ forloop.counter }}-{{ abc }}</li>
{% endif %}

{% endfor %}  
</ul>

{% endblock %}
```

Syntax Conditions:

```
{% if bool_expression %}
...
{% elif bool_expression %}
...
{% else %}
...
{% endif %}
``` 

## Template Tags and Filters

```
{% extends 'base.html' %}

{% block shop_list %}

<h1>This is a shop list !!!</h1>
<h2>{{title|capfirst|upper}}</h2>

{{ my_html|safe }}

<ul>{% for ind in kittens %}
    {% if ind == "Rafael" %}
    <li>HEEEY!!! It's the best dog's name! <div class="emphasize_text">{{ind}}</div></li>
    {% else %}
    <li>{{ ind|add:" nice touch :)"|capfirst }}</li>
    {% endif %}
    {% endfor %}
</ul>


{% endblock shop_list %}
```

Here `{{ my_html|safe }}` we passed a variable `my_html` which contains html code in ""

|safe filter makes it html code, not a string in our template

Like any filter you can use them with `|` (pipe) sign

All of them are in documentation. Here's just a brief example what you can do with them.


## Render Data from the Data Base with a Model

You can get your obj in django shell

Run `python3 manage.py shell` in your command line

Run these commands:
```
>>> from products.models import Product
>>> Product.objects.get(id=1)
<Product: Product object (1)>
>>> obj = Product.objects.get(id=1)
>>> dir(obj)
```

`dir(obj)` method will return all the attributes and methods this obj has

Now exit the shell with `exit()` command and create in products/views.py a view function
That's where we will render our data

In products/views write:
```
from django.shortcuts import render

from .models import Product

# Create your views here.
def product_detail_view(request):
    obj = Product.objects.get(id=1)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description
    # }
    context = {
        "object": obj
    }

    return render(request, "product/detail.html", context)

```

add this code to trydjango/urls.py:
```
from products/models import Product

urlpatterns = [
    path('', home_view, name='home'),
    ...
    path('product/', product_detail_view)
]
```
create a new folder `product` in templates folder and create a `detail.html` file

add this code to detail.html:
```
{% extends 'base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<p> {% if object.description is not None and object.description != '' %}{{ object.description }}{% else %}Description Coming Soon{% endif %}</p>
{% endblock %}
```

## How Django Templates Load with Apps

* Create a folder `/templates/products' in products app
* Crete a new template `product_detail.html` in that folder
```
# /src/products/templates/products/product_detail.html
{% extends 'base.html' %}

{% block content %}
<h1>In App template: {{object.title}}</h1>
<p> {% if object.description is not None and object.description != '' %}{{ object.description }}{% else %}Description Coming Soon{% endif %}</p>
{% endblock %}
```
* Don't forget to add {% block content %}{% endblock %} in the `base.html` file(path: /src/templates/base.html)

> Remember that if you're doing a solo project or if you're having a team, you need to keep app templates in app folder and not in /src/templates cause otherwise it'll be confusing

## Django Models Forms
Create in any app(here it is products app) a new file `forms.py`

Paste this code:
```
# /src/products/forms.py
from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]
```
When choosing a name for a class there are several preferable names for that:
* ProductModelForm
* ProductForm
* ProductCreateForm

Then render this out in the products/views.py

Create a template in /src/products/templates/products/product_create.html
Paste this code:
```
{% extends 'base.html' %}

{% block content %}
<form method='POST'> {% csrf_token %}
    {{ form.as_p }}
    <input type='submit' value='Save' />
</form>
{% endblock %}
```

Then create a new product_create_view() func in /products/views.py
```
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
        "form": form
    }

    return render(request, 'products/product_create.html', context)
```

Then bring it in into our urls /src/trydjango/ursl.py

```
...
from products.views import product_create_view

urlpatterns = [
    path('', home_view, name='home'),
    ...
    path('create/', product_create_view)
]
```

## Raw HTML Forms

Get rid of django forms:

```
# /products/templates/products/product_create.html
{% extends 'base.html' %}

{% block content %}
<form method='POST'> 
    {% csrf_token %} --- delete
    {{ form.as_p }}  --- delete
    <input type='submit' value='Save' />
</form>
{% endblock %}
```

Action will send the form to any url you put there

Paste this code to /products/views.py:
```
def product_create_view(request):
    if request.method == "POST":
        my_new_title = request.POST.get('title')
        print(my_new_title)
        # Product.objects.create(title=my_new_title)
    context = {}
    return render(request, 'products/product_create.html', context)
```
Also the final product_create.html file look:

```buildoutcfg
{% extends 'base.html' %}

{% block content %}
<form action="." method='POST'> 
    {% csrf_token %}
    <input type="text" name="title" placeholder="Your Title" />
    <input type='submit' value='Save' />
</form>
{% endblock %}
```

It's a bad method of saving data because we're not validating if this good data, we're not cleaning this data. So we need to make sure that we do that

## Pure Django Form

Go to src/products/forms.py and paste:
```buildoutcfg
class ProductRawForm(forms.Form):
    title       = forms.CharField()
    description = forms.CharField()
    price       = forms.DecimalField()
```

If you try to declare title or description fields to forms.TextField  it's not going to work
[Check out the documentation](https://docs.djangoproject.com/en/3.2/ref/forms/fields/)

Then import this form in /src/products/views.py
```buildoutcfg
from .forms import ProductForm, ProductRawForm

# ... Other code

def product_create_view(request):
    my_form = ProductRawForm()
    context = {
        "form": my_form
    }
    return render(request, 'products/product_create.html', context)
```

Paste this code to /src/products/templates/products/create_product.html:
```buildoutcfg
{% extends 'base.html' %}

{% block content %}
<form action="." method='POST'> 
    {% csrf_token %}
    {{ form.as_p }} <!--as_p just renders it out in <p></p> tags -->
    <!--You could as well use forms.as_ul to render it as unordered list -->
    <input type='submit' value='Save' />
</form>
{% endblock %}
```

The final look of /src/products/views.py:
```buildoutcfg
def product_create_view(request):
    my_form = RawProductForm()
    if request.method == "POST":
        my_form = RawProductForm(request.POST)
        if my_form.is_valid():
            # now the data is good
            print(my_form.cleaned_data)
            Product.objects.create(**my_form.cleaned_data)
        else:
            print(my_form.errors)
    context = {
        "form": my_form
    }
    return render(request, 'products/product_create.html', context)
```
##Form Widgets

Pate this code in /src/products/forms.py:
```buildoutcfg
class RawProductForm(forms.Form):
    title       = forms.CharField(required=True, label='Too Too Too')
    description = forms.CharField(required=False, widget=forms.Textarea)
    price       = forms.DecimalField(initial=199.99)
```
Check out all the various widgets [here](https://docs.djangoproject.com/en/3.2/ref/forms/widgets/)

The final changes in forms.py:
```buildoutcfg

class RawProductForm(forms.Form):
    title       = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    description = forms.CharField(
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description",
                                    "class":"new-class name",
                                    "id": "my-id-for-text-area",
                                    "rows": 20,
                                    "cols": 120
                                }
                            )
                        )
    price       = forms.DecimalField(initial=199.99)
```

## Form Validation Methods
If you want to validate a specific form field before saving it to db first paste 
this code to views.py  
```
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid(): # Will check if there are functions like clean_<field_name> function in your forms func
        form.save() 
        form = ProductForm()

    context = {
        "form": form
    }

    return render(request, 'products/product_create.html', context)
```
In your forms.py paste this after Meta class but not inside of it:
```buildoutcfg
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "CFE" in title:
            return title
        else:
            raise forms.ValidationError("This is not a valid title")
```

Look at the final forms.py file:
```buildoutcfg
from django import forms

from .models import Product

class ProductForm( forms.ModelForm):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Your description",
                "class": "new-class name",
                "id": "my-id-for-text-area",
                "rows": 20,
                "cols": 120
            }
        )
    )
    price = forms.DecimalField(initial=199.99)
    email = forms.EmailField()
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "CFE" not in title:
            raise forms.ValidationError("This is not a valid title")
        if "news" not in title:
            raise forms.ValidationError("This is not a valid title")
        return title

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if "edu" not in email:
            raise forms.ValidationError("This is not a valid email")
        return email
```

## Initial Values for Forms

In views.py example code:
```buildoutcfg
def render_initial_data(request):
    initial_data = {
        'title': "My this awesome title"
    }
    obj = Product.objects.get(id=1)
    form = ProductForm(request.POST or None, initial=initial_data, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        "form": form
    }
    return render(request, "products/product_create.html", context)

```
--> `form = ProductForm(request.POST or None, initial=initial_data, instance=obj)`

Here initial attribute defines intial values for the form.py to fill in the form

__Always validate the data before posting it in db__
```buildoutcfg
if form.is_valid():
        form.save()
```

__Don't forget to add render_initial_data function in urls.py__

## Dynamic URL Routing

Changed product_detail.html. Now it looks like this:
```
{% extends 'base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<p>{{object.description}}</p>
<p>{{object.price}}</p>
{% endblock %}
```
In views.py dynamic function:
```buildoutcfg
def dynamic_lookup_view(request, id):
    obj = Product.objects.get(id=id)
    context = {
        "object": obj
    }
    return render(request, 'products/product_detail.html', context)
```
In urls.py:
```buildoutcfg
urlpatterns = [
    path('products/<int:id>/', dynamic_lookup_view)
    ...
    ]
```
It passes a new argument to our view. So our view has request argument by default.
It passes in a new argument of id, which we declare a name of.

If you change a name of id in url.py, you also need to change it in view

## Handle DoesNotExist
The long way to handle DoesNotExist exception if writing try/except block:

```buildoutcfg
from django.http import Http404
from django.shortcuts import render

from .models import Product

def dynamic_lookup_view(request, id):
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    context = {
        "object": obj
    }
    return render(request, 'products/product_detail.html', context)
```

The easier and probably better way to do it is by importing this method:
```buildoutcfg
from django.shortcuts import render, get_object_or_404

from .models import Product

def dynamic_lookup_view(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {
        "object": obj
    }
    return render(request, 'products/product_detail.html', context)

```

## Delete and Confirm

Created a new template /src/products/templates/products/product_delete:
```buildoutcfg
{% extends "base.html" %}

{% block content %}

<form action="." method="POST">{% csrf_token %}
    <h1>Do you want to delete the product "{{ object.title }}"?</h1>
    <p><input type="submit" value="Yes" /> <a href="../">Cancel</a></p>
</form>

{% endblock %}
```

And views.py :
```buildoutcfg
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product
from .forms import ProductForm, RawProductForm


# Create your views here

def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        # confirming delete
        obj.delete()
        return redirect('../../')
    context = {"object": obj}
    return render(request, "products/product_delete.html", context)
```

So I ran into a really frustrating error. 
When I added path to the urls I forgot to put `/` at the end of it and instead of
`path('products/<int:id>/delete/'` I put `path('products/<int:id>/delete'`. So be aware of it!!!

There's also `redirect` function that basically redirects the user after deleting an object

## View a list of Database Objects

In products/views.py we set queryset variable to our Product.objects.all()

Instead of Product can be any model object that you created in your app/models.py

```buildoutcfg
def product_list_view(request):
    queryset = Product.objects.all() # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, 'products/product_list.html', context)
```

Created a new template for that – product_list.html:
```buildoutcfg
{% extends 'base.html' %}

{% block content %}
<h1>Product List</h1>
{% for instance in object_list %}
    <p>{{ instance.id }} - {{ instance.title }}</p>
{% endfor %}

{% endblock %}
```

## Dynamic Linking of URLs

Instead of rewriting the dynamic url every time you change the path in views.py you can
make Dynamic Linking of URLs

Define in your models.py file a new method get_absolute_path and return the string value
```buildoutcfg
# models.py

from django.db import models

# Create your models here.

class Product(models.Model): 
    title = models.CharField(max_length=120) 
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f"/products/{self.id}/"
```
That's how product_list.html file look like now:
```
{% extends 'base.html' %}

{% block content %}
<h1>Product List</h1>
{% for instance in object_list %}
    <p>{{ instance.id }} - <a href="{{ instance.get_absolute_url }}">{{ instance.title }}</a></p>
{% endfor %}

{% endblock %}
```

## Django URLs Reverse

To transition our get_absolute_url method in models.py to being dynamic itself

For that we need to use function called reverse

```buildoutcfg
# models.py
from django.db import models
from django.urls import reverse
# Create your models here.

class Product(models.Model): 
    title = models.CharField(max_length=120) 
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)

    def get_absolute_url(self):
        # return f"/products/{self.id}/"
        return reverse("product-detail", kwargs={"id": self.id})
```

We also assign name attribute in urls.py:
```buildoutcfg
urlpatterns = [
    path('products/<int:id>/', dynamic_lookup_view, name="product-detail"),
    path('products/<int:id>/delete/', product_delete_view, name="porduct-delete"),
    path('products/', product_list_view, name="product_list")
]
```
Whatever we change our url for, where a function get_absolute_url is used it'll return us the exact url we need

## In App URLs and Namespacing

Create urls.py file in products and import all the relative views functions

```buildoutcfg
# products/urls.py
from django.contrib import admin
from django.urls import path

from pages.views import home_view, about_view, shoplist_view
from products.views import (
    product_detail_view,
    product_delete_view,
    product_list_view,
    product_update_view,
    product_create_view,
)

urlpatterns = [
    path('products/<int:id>/delete/', product_delete_view, name="product-delete"),
    path('products/', product_list_view, name="product_list"),
    path('products/<int:id>/', product_detail_view, name="product-detail"),
    path('products/create/', product_create_view)
]
```

1. Import the include() function: from django.urls import include, path
2. Add a URL to urlpatterns:  path('products/', include('products.urls'))

```buildoutcfg
# trydjango/urls.py
from django.contrib import admin
from django.urls import include, path

from pages.views import home_view, about_view, shoplist_view

urlpatterns = [
    path('products/', include('products.urls')),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('about/', about_view),
    path('shoplist/', shoplist_view),
]
```

But it's not really going to work the way that we want. In this case we need to get rid of `'products/...'` products
because it's already being rendered with 'products/' fromm trydjango/urls.py file

```buildoutcfg
from django.contrib import admin
from django.urls import path

from pages.views import home_view, about_view, shoplist_view
from products.views import (
    product_detail_view,
    product_delete_view,
    product_list_view,
    product_update_view,
    product_create_view,
)

app_name = 'products'

urlpatterns = [
    path('<int:id>/delete/', product_delete_view, name="product-delete"),
    path('', product_list_view, name="product_list"),
    path('<int:id>/', product_detail_view, name="product-detail"),
    path('create/', product_create_view)
]
```

As you might see, we also added a new variable `app_name`. Don't get startled.
It contains the namespace of our app

Then you need to add this line to your code in products/models.py
```buildoutcfg
# products/models.py
from django.db import models
from django.urls import reverse
# Create your models here.

class Product(models.Model): 
    title = models.CharField(max_length=120) 
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"id": self.id})
```

In a function get_absolute_url instead of a line
```buildoutcfg
return reverse("product-detail", kwargs={"id": self.id})
```
We return this line
```buildoutcfg
return reverse("products:product-detail", kwargs={"id": self.id})
```
Because products is the name of our app and spacename

## ERRORS

### OperationalError at /admin/products/product/add/

Solution:
```
pip install django==2.1.5
```
### products.Product.title: (fields.E120) CharFields must define a 'max_length' attribute.

```
# Create your models here.
class Product(models.Model):
    title       = __models.CharField() # max_length = required__
    description = models.TextField()
    price       = models.TextField()
    summary     = models.TextField(default='this is cool!')

# title = models.CharField(max_length=120) --> You must set max_width attribute in models.CharField() field type
```
### You are trying to add a non-nullable field 'featured' to product
This happens after changing the model of an APP without making any changes to the previous objects of this model in a database

Previous model:
```
# Create your models here.
class Product(models.Model):
    title       = __models.CharField() # max_length = required__
    description = models.TextField()
    price       = models.TextField()
    summary     = models.TextField(default='this is cool!')
```
Current model:
```
# reate your models here.
class Product(models.Model):
    title       = models.CharField(max_length=120) # max_length = required
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(decimal_places=2, max_digits=10000)
    summary     = models.TextField()
    featured    = models.BooleanField()
```
There's at least two solutions
```
featured = models.BooleanField(null=True)
```
Leaves this field empty in all the previous objects
```
featured = models.BooleanField(default=True)
```
Sets this field to true in all the previous objects

Choose one of the options provided in the shell
```
1
True
```

### OperationalError at /admin/products/product/ no such column: products_product.featured:
```
python manage.py makemigrations
python manage.py migrate
```

### TemplateDoesNotExist at /products/

Look at these lines:

```
Template-loader postmortem

Django tried loading these templates, in this order:

Using engine django:
django.template.loaders.filesystem.Loader: /Users/andreimardash/pro/trydjango/src/templates/products/produc_detail.html (Source does not exist)

django.template.loaders.app_directories.Loader: /usr/local/lib/python3.7/site-packages/django/contrib/admin/templates/products/produc_detail.html (Source does not exist)

django.template.loaders.app_directories.Loader: /usr/local/lib/python3.7/site-packages/django/contrib/auth/templates/products/produc_detail.html (Source does not exist)

django.template.loaders.app_directories.Loader: /Users/andreimardash/pro/trydjango/src/products/templates/products/produc_detail.html (Source does not exist)
```

### Solution

Check the path you used in product/views.py with the actual file you want to render
They must be different

### TypeError at /products/10/ 
__`dynamic_lookup_view() got an unexpected keyword argument 'id'`__

Our view function just doesn't know what argument `id` is. So all you have to do is just to make sure that
you're passing the right argument, for example:
in urls.py
```buildoutcfg
urlpatterns = [
    path('products/<int:id>/', dynamic_lookup_view)
```
And in views.py
```buildoutcfg
def dynamic_lookup_view(request, my_id):
    obj = Product.objects.get(id=my_id)
    context = {
        "object": obj
    }
    return render(request, 'products/product_detail.html', context)
```
You need to change `my_id` in dynamic_lookup_view function to `id`
That'll do