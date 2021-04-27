from django.db import models

# Create your models here.

class Product(models.Model): 
    title = models.TextField() 
    description = models.TextField() 
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    summary = models.TextField()
    quantity = models.DecimalField(decimal_places=0, max_digits=30)