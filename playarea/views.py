from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def say_hello(request):
    return render(request, 'playarea/home.html',{'name':"Muataz"})

def return_page(request):
    return render(request,'playarea/new.html',{'phone':99840823})