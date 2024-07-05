from django.shortcuts import render
from .models import Mobile

# Create your views here.
def product(request):
        


        products = Mobile.objects.all()
        return render(request,"index.html",{"products":products})


