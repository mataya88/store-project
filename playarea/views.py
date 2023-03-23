from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product
# Create your views here.



def say_hello(request):
    queryset = Product.objects.filter(unit_price__lt=5)

    return render(request, 
    'playarea/home.html',
    {'name':"Muataz",
    "products":list(queryset)})

def return_page(request):
    return render(request,'playarea/new.html',{'phone':99840823})