from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mobile, wishlist, Cart, address, cart_orders
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
    
@login_required

def checkout_page(request):
    user = request.user
     
    addresses = address.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.price for item in cart_items)
    delivery_charges = 40
    total_amount = total_price + delivery_charges

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        try:
            selected_address = address.objects.get(id=selected_address_id)
        except address.DoesNotExist:
            # Handle the error appropriately
            return render(request, 'checkout.html', {
                "addresses": addresses,
                'cart_items': cart_items, 
                'total_price': total_price, 
                'total_amount': total_amount, 
                'delivery_charges': delivery_charges,
                'error': 'The selected address does not exist.'
            })

        for item in cart_items:
            cart_order = cart_orders(user=user, order=item, address=selected_address)
            cart_order.save()
        
        # Clear the cart after ordering
        cart_items.delete()

        return redirect('order_success')  # Change to a success page or wherever you want to redirect

    return render(request, 'checkout.html', {
        "addresses": addresses,
        'cart_items': cart_items, 
        'total_price': total_price, 
        'total_amount': total_amount, 
        'delivery_charges': delivery_charges
    })

def address_page(request):
    user = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        village = request.POST.get("village")
        colony = request.POST.get("colony")
        state = request.POST.get("state")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")

        if not all([first_name, phone, email, village, colony, state, city, pin_code]):
            messages.error(request, "All fields are required.")
        else:
            address.objects.create(
                user=user,
                first_name=first_name,
                mobile_number=phone,
                email=email,
                village=village,
                colony=colony,
                state=state,
                city=city,
                pin_code=pin_code
            )
            messages.success(request, "Address saved successfully.")
            return redirect('checkout_page')  # Adjust the redirect as needed
    
    return render(request, 'address.html')

def delete_address(request,address_id):
     user = request.user
     Address1 = address.objects.filter(user=user, id=address_id)
     Address1.delete()
     return redirect('checkout_page')

def order_page(request):
     user = request.user
     orders = cart_orders.objects.filter(user=user)
     return render('order_page.html')

def order_success(request):
     return render(request, "order_success.html")

def back_to_home(request):
    return render(request, 'cart.html')



     


