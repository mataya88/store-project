from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=15)
    featured_product = models.OneToOneField('Product', 
                        on_delete=models.SET_NULL, null=True,
                        related_name='+') 
                        # '+' will cancel the reverse relationship

class Product(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(decimal_places=3,blank=False, null=True,max_digits=6)
    inventory = models.PositiveIntegerField(blank=False, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True,on_delete=models.SET_NULL)
    slug = models.SlugField()

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, blank=False, null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False)

class Customer(models.Model):
    BRONZE = 'B'
    GOLD = 'G'
    SILVER = 'S'
    MEMBERSHIP_CHOICES = [(GOLD,"Gold"),(SILVER,"Silver"),(BRONZE,"Bronze")]
    first_name = models.CharField(max_length =20, blank=False, null=True)
    last_name = models.CharField(max_length=20, blank=False, null=True)
    email = models.EmailField(blank=False, null=True, unique=True)
    birth_date = models.DateField(auto_now_add=True,null=True)
    phone = models.PositiveIntegerField(max_length=8,blank=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,
                 default=BRONZE)

class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    STATUS_CHOICES = [(PENDING_STATUS,"Pending"),(COMPLETE_STATUS,"Complete"),(FAILED_STATUS,"Failed")]
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices= STATUS_CHOICES)
    
    

class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(blank=False)
    unit_price = models.DecimalField(decimal_places=3,blank=False,max_digits=6)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
