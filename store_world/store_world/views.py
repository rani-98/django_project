from django.http import HttpResponse
from django.shortcuts import render



def home(request):
    print("i am in home page")
    return HttpResponse("Hello, World!")

def example(request):
    return render(request,"example.html")



