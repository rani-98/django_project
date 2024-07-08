from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mobile, wishlist, Cart
import json
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def product(request):

        products = Mobile.objects.all()
        user=request.user

        for product in products:
              product.is_wished = False
        # check if the shirt is in the wishlist
              if product.wishlist.filter(user=user).exists():
                   product.is_wished = True
                   print("product.is_wished", product.is_wished)

        return render(request,"index.html",{"products":products})



def productInfo(request,product_id):
       
        product = Mobile.objects.filter(id=product_id)
        return render(request,"product.html",{"product":product})
@csrf_protect
def add_to_wishlist(request,product_id):

    if not product_id:
        return JsonResponse({"error": "product_id is required"})
    user = request.user

    # get the mobile object from the shirt id
    mobile = Mobile.objects.get(id=product_id)
    # create a wishlist object
    whish = wishlist(mobile=mobile,user=user)

    # save the wishlist object
    whish.save()

    return JsonResponse({"success": "mobile added to wishlist"})


@csrf_protect
def Remove_from_Wishlist(request, product_id):

    if not product_id:
        return JsonResponse({"error": "mobile is required"})
    user=request.user
    

    mobile = Mobile.objects.get(id=product_id)
    # remove the mobile from the wishlist
    wishlist.objects.filter(mobile=mobile,user=user).delete()

    return JsonResponse({"success": "mobile removed from wishlist"})




def cart_view(request):
        
        cart = Cart.objects.all()
        total_price = sum(item.price for item in cart)

        context = {
                'cart': cart,
                'total_price': total_price,
        }
        return render(request,"cart.html", context)

@login_required
@csrf_protect
def add_to_cart(request, product_id):
    if not product_id:
        return JsonResponse({"error": "product_id is invalid"})

    user = request.user

    cart = Cart.objects.filter(id=product_id, user=user)

    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()

        return JsonResponse({"success": "mobile added to cart","redirect_url" : " "})

    mobile = Mobile.objects.get(id=product_id)
    cart = Cart(mobile=mobile, user=user, price=mobile.discountPrice)
    cart.save()

    return JsonResponse({"success": "mobile added to cart", "redirect_url" : " " })


@login_required
@csrf_protect
def remove_from_cart(request, product_id):
    if not product_id:
        return JsonResponse({"error": "product_id is invalid"})

    user = request.user

    cart = Cart.objects.filter(id=product_id, user=user)

    if cart.exists():
        cart = cart.first()
        cart.quantity -= 1
        if cart.quantity <= 0:
            cart.delete()
            



        else: 
            cart.save()

    
        return JsonResponse({"success": "product removed from cart", "redirect_url" : " " })
    

   

