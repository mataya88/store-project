from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F
from store.models import *
from django.db.models.aggregates import Count, Sum, Min, Max, Avg

# Create your views here.



def say_hello(request):
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    result = Product.objects.aggregate(count = Count('pk'), min_price = Min('unit_price'))
    return render(request, 
    'playarea/home.html',
    {'name':"Muataz",
    "products":[],
    'result':result})

def return_page(request):
    return render(request,'playarea/new.html',{'phone':99840823})