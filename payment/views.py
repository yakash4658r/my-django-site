import os

from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseBadRequest
from .form import ShippingAddressForm
from .models import *
from cart.cart import Cart
from django.conf import settings
import razorpay
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address_id = form.save()
            address = ShippingAddress.objects.get(pk=address_id.pk)

            order = Order.objects.create(user=request.user,address=address,)
            return redirect("billing_info",order.pk)

    else:
        form = ShippingAddressForm()



    context = {
        "form":form,
        "products":cart.products()
    }
    return render(request,"checkout.html",context)

def billing_info(request,pk):
    cart = Cart(request)
    order = Order.objects.get(pk=pk)
    context = {
        "products":cart.products(),
        "order":order
    }
    return render(request,"billing_info.html",context)

@login_required
def proccess_order(request,pk):
    cart = Cart(request)
    products = cart.products()
    # added divlivery charge
    total_amount = cart.total() + 100

    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID,settings.RAZOR_PAY_SECRET_KEY))

    data = {
        "amount":(int(total_amount) * 100),
        "currency":"INR",
        "payment_capture":"1"
    }

    razorpay_order = client.order.create(data)


    order = Order.objects.get(pk=pk)
    order.order_id = razorpay_order["id"]
    order.amount_paid = total_amount
    order.save()

    for product,qty in products.items():
        if product.is_discount:
            product_price = product.discount_price
        else:
            product_price = product.price

        OrderItems.objects.create(
            order = order,
            product = product,
            product_name= product.name,
            product_price = product_price,
            product_qty= qty,
            product_size=product.size
        )
    if os.environ.get("ENVIRONMENT") == "production":
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL)).replace("http://", "https://")
    else:
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))

    return JsonResponse({
            "order_id":razorpay_order["id"],
            "razorpay_key_id":settings.RAZOR_PAY_KEY_ID,
            "product_name":request.user.username,
            "amount":razorpay_order["amount"],
            "callback_url": callback_url,
        })

@csrf_exempt
def payment_verify(request):

    if "razorpay_signature" in request.POST:
        client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID,settings.RAZOR_PAY_SECRET_KEY))

        order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature  = request.POST.get("razorpay_signature")

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            # Payment verified successfully
            order = Order.objects.get(order_id=order_id)
            order.is_paid = True
            order.payment_id = razorpay_payment_id
            order.signature = razorpay_signature
            order.save()

            items = OrderItems.objects.filter(order=order)

            for order_item in items:
                product = order_item.product
                product.no_of_sales += 1
                product.save()


            if "session_key" in request.session:
                del request.session["session_key"]


            return render(request,"payment_verify.html",{"status": "Payment Verified Successfully","order_id":order_id})
            # return redirect("confirm_order",order_id)
        except razorpay.errors.SignatureVerificationError:

            return render(request,"payment_verify.html",{"status":"Payment verification failed"})

    return render(request,"payment_verify.html",{"status":"Invalid Request"})


def update_address(request,order_pk,pk):

    address = ShippingAddress.objects.get(pk=pk)
    form = ShippingAddressForm(instance=address)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            return redirect("billing_info", order_pk)
    return render(request,"checkout.html",{"form":form})

def confirm_order(request,order_id):

    return render(request,"payment_verify.html",{"status": "Payment Verified Successfully","order_id":order_id})
