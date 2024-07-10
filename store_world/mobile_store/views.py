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
    user = request.user
    carts = Cart.objects.filter(user=user)
    orders = cart_orders.objects.filter(user=user)
    ordered_mobile_ids = set(order.order.mobile.id for order in orders)

    # Calculate total price for each cart item
    for cart in carts:
        cart.price_per_cart = cart.quantity * cart.mobile.discountPrice
        cart.ordered = cart.mobile.id in ordered_mobile_ids  # Check if the item has been ordered

    total_price = sum(cart.price_per_cart for cart in carts)

    return render(request, 'cart.html', {'carts': carts, 'total_price': total_price})

@login_required
@csrf_protect
def add_to_cart(request, product_id):
    if not product_id:
        return JsonResponse({"error": "product_id is invalid"})

    user = request.user

    cart = Cart.objects.filter(id=product_id, user=user)
    price_per_cart = 0
    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
        price_per_cart = cart.quantity *cart.price + price_per_cart

        return JsonResponse({"success": "mobile added to cart","redirect_url" : " ", "price_per_cart" : price_per_cart})

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
        for address in selected_address:
            address.name = address.first_name
            address.mobile_number = address. mobile_number
            address.email = address.email
            address.village = address.village
            address.city = address.city
            address.colony = address.colony
            address.state = address.state
            address.pin_code = address.pin_code

        address = f"{address.name}, {address.mobile_number}, {address.email}, {address.village}, {address.city}, {address.colony}, {address.state},{address.pin_code}"

        for item in cart_items:
            cart_orders.objects.create(user=user, order=item, address=selected_address, )
        #cart_items.delete()
        # Clear the cart after ordering
            

        return redirect('product')  # Change to a success page or wherever you want to redirect

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
    orders = cart_orders.objects.filter(user=user).select_related('order__mobile', 'address')

    return render(request, 'order_page.html', {'orders': orders})

def order_success(request):
     return render(request, "order_success.html")

def back_to_home(request):
    return render(request, 'cart.html')






     


