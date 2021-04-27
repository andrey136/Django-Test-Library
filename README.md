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
