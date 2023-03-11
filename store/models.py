from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=15)

class Product(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(blank=False, null=True)
    inventory = models.IntegerField(blank=False, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=False)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, blank=False, null=True)
    product = models.ForeignKey(Product, blank=True, null=True)
    quantity = models.IntegerField()

class Customer(models.Model):
    first_name = models.CharField(max_length =20, blank=False, null=True)
    last_name = models.CharField(max_length=20, blank=False, null=True)
    email = models.EmailField(blank=False, null=True, unique=True)
    birth_date = models.DateField(auto_now_add=True,null=True)
    phone = models.IntegerField(max_length=8,blank=True)
