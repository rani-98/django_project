from django.shortcuts import render
from .models import Mobile

# Create your views here.
def product(request):

        products = Mobile.objects.all()
        return render(request,"index.html",{"products":products})


def productInfo(request,product_id):
       
        product = Mobile.objects.filter(id=product_id)
        return render(request,"product.html",{"product":product})

def cart(request):
        cart = Mobile.objects.all()
        return render(request,"cart.html",{"cart":cart})
