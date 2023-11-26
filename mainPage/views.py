from django.shortcuts import render
from .models import *

def home (response):
    products = Products.objects.all()
    firstProduct = Products(name="Denim") #the name can be adapted
    return render(response, "main/home.html", {"products":products,"firstProduct":firstProduct,})

def about (response):
    
    return render(response, "main/about.html", {})