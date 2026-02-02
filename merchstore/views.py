from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings

from merchstore.models import Category, Product, CartItem, OrderItem, Order
from merchstore.forms import OrderDeliveryForm

from merchstore.mesmailh import merchOrderConfirmationMail
from merchstore.mespayments import create_checkout_session, retrieve_checkout_session

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

import json
# Create your views here.

def merchHome(request):
    categories = Category.objects.all()
    # products = Product.objects.all()
    q = request.GET.get('search')
    if q == None:
        q = ''
    products = Product.objects.filter(Q(name__icontains=q)|Q(desc__icontains=q)|Q(category__name__icontains=q)|Q(category__desc__icontains=q)).order_by('name','desc')
    count = products.count()
    # add search functionality later
    context = {"products": products, "categories": categories, "count":count}
    return render(request, 'merchstore/products.html', context)

def merchProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except:
        return HttpResponse("Product not found")
    
    context = {"product":product}
    return render(request, 'merchstore/single-product.html',context)

@login_required(login_url="centBaseLoginUser")
def merchCart(request):
    cartItems = CartItem.objects.filter(user=request.user)
    cart_total = 0
    total_items = 0
    for cartItem in cartItems:
        cart_total+=cartItem.item_qty_price()
        total_items+= cartItem.qty

    context = {'cartItems': cartItems,'products_added':cartItems.count() ,'total_items': total_items,'cart_total': cart_total}
    return render(request, 'merchstore/cart.html', context)

@login_required(login_url="centBaseLoginUser")
def merchUpdateCart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        productId = data['productId']
        productAction = data['productAction']

        success = True
        try:
            product = Product.objects.get(id=productId)
            cartItem, created = CartItem.objects.get_or_create(user=request.user, prod=product)
        except:
            success = False
            return JsonResponse({'success':success})

        if not product.available:
            return HttpResponse("Not available")

        full = False

        if productAction == "add":
            if(cartItem.qty < cartItem.prod.cart_max):
                cartItem.qty = (cartItem.qty + 1)
            else:
                success = False
                full = True
        elif productAction == "reduct":
            if(cartItem.qty >=1 ):
                cartItem.qty = (cartItem.qty - 1)
            else:
                success = False

        cartItem.save()

        if cartItem.qty <= 0:
            cartItem.delete()

        # return JsonResponse(f"Server resp: {productAction} {productId}", safe=False)
        ctxDict = {
            'updPId': productId,
            'prodName': product.name, #added later
            'updQty': cartItem.qty,
            'updPrice': cartItem.item_qty_price(),
            'success': success,
            'full': full
        }
        return JsonResponse(ctxDict)
    else:
        return HttpResponse("Invalid request")

@login_required(login_url="centBaseLoginUser")
def merchCheckout(request):
    if request.method=='POST':
        order_form = OrderDeliveryForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()

            cartItems = CartItem.objects.filter(user=request.user)
            order_items = []
            for cartItem in cartItems:
                if cartItem.prod.isOnSale():
                    itemprice = cartItem.prod.sale_price
                else:
                    itemprice = cartItem.prod.price
                # itemprice = cartItem.prod.actualPrice()
                order_items.append(OrderItem(order=order, prod=cartItem.prod, qty=cartItem.qty, price=itemprice))
            
            # create in bulk from the list of objects above
            OrderItem.objects.bulk_create(order_items)
            # delete the cart items to reset the cart
            cartItems.delete()

            if not settings.STRIPE_KEYS_SET:
                messages.success(request,"Your order has been placed.")
                merchOrderConfirmationMail(request.user, order)
                return redirect('merchStoreOrders')
            else:
                payment_method = order_form.cleaned_data['payment_method']
                if payment_method == 'method_stripe':
                    session = create_checkout_session(order)
                    order.stripe_session_id = session.id
                    order.save(update_fields=['stripe_session_id'])
                    return redirect(session.url)
                else:
                    messages.success(request,"Your order has been placed.")
                    merchOrderConfirmationMail(request.user, order)
                    return redirect('merchStoreOrders')
                
    profile = request.user.profile
    cartItems = CartItem.objects.filter(user=request.user)
    cart_total = 0
    total_items = 0
    for cartItem in cartItems:
        cart_total+=cartItem.item_qty_price()
        total_items+= cartItem.qty

    initial_form_fields = {'phone': profile.phone,'uemail':profile.user.email,'street': profile.street, 'address': profile.address,'city': profile.city, 'country': profile.country, 'zipcode': profile.zipcode}
    order_form = OrderDeliveryForm(initial=initial_form_fields)    
    context = {'order_form': order_form, 'cartItems': cartItems, 'cart_total': cart_total, 'total_items': total_items}
    if(total_items>0):
        return render(request, 'merchstore/checkout.html', context)
    else:
        messages.warning(request, "Add some items to your cart to checkout.")
        return redirect('merchStoreCart')
 

@login_required
def confirmMerchPayment(request):
    if not settings.STRIPE_KEYS_SET:
        return HttpResponse("Stripe not configured")

    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponse("No session id provided")

    session = retrieve_checkout_session(session_id)
    try:
        order = Order.objects.get(stripe_session_id=session_id, user=request.user)
    except:
        return HttpResponse("Order not found")

    if order.payment_status == 'PAID':
        return redirect('merchStoreOrders')

    if session.payment_status == 'paid':
        messages.success(request,"Payment Successful. Your order has been placed.")
        order.payment_status = 'PAID'
    else:
        messages.info(request, "Payment Failed. Your order has been placed and converted to cash on delivery. Feel free to contact us for any help.")

    merchOrderConfirmationMail(request.user, order)
    order.save(update_fields=['payment_status'])
    return redirect('merchStoreOrders')

@login_required(login_url="centBaseLoginUser")
def merchOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('delivered','-created_at')
    # orderItems = []
    # for order in orders:
    #     orderItems+=order.objects.orderItems_set.all() 
    context = {'orders': orders, 'ord_count': orders.count()}
    return render(request, 'merchstore/orders.html', context)

