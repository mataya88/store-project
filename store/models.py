from django.db import models
from django.core.validators import MinValueValidator

class Promotion(models.Model):
    description = models.CharField(max_length=255) #TextField ok
    discount = models.FloatField()
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    featured_product = models.OneToOneField(
        'Product', on_delete=models.SET_NULL, 
        null = True, related_name='+'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    slug = models.SlugField()

    class Meta:
        ordering = ['title'] # The default ordering for the admin page
        verbose_name = 'MY PRODUCTS'
        verbose_name_plural = 'THE PRODUCTS'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    reviewer_name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    
class Customer(models.Model):
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'
    
    MEMBERSHIP_COICES = [
        (BRONZE_MEMBERSHIP, 'Bronze'),
        (SILVER_MEMBERSHIP, 'Silver'),
        (GOLD_MEMBERSHIP, 'Gold')
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(auto_now_add=True, null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_COICES,
        default=BRONZE_MEMBERSHIP
        )
    #address_set
 
    def __str__(self):
        return self.first_name + ' ' + self.last_name
 

class Address(models.Model):
    street = models.CharField(max_length=255)   
    city = models.CharField(max_length=255)
    zip_f = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)  
     
class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PENDING_STATUS, 'Pending'),
        (COMPLETE_STATUS, 'Complete'),
        (FAILED_STATUS, 'Failed')
    ] 
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length = 1, choices=PAYMENT_STATUS_CHOICES,
        default=PENDING_STATUS
    )
    customer= models.ForeignKey(Customer, on_delete=models.PROTECT)
    
class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()   #PositiveIntegerField ok
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField()   #PositiveIntegerField ok
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)