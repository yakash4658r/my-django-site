from django.shortcuts import render, get_object_or_404,redirect

from payment.models import Order,OrderItems
from payment.views import billing_info
from .models import Product, CustomerForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
# Create your views here.
def home(request):
    try:
        product = Product.objects.all().order_by("-no_of_sales")[:4]
    except Exception as e:
        product = None

    context = {
        "best_products":product
    }
    return render(request,"index.html",context)


def terms(request):
    return render(request,"terms.html")

def shipping_page(request):
    return render(request, "shipping_page.html")


def policy(request):
    return render(request,"privacy_policy.html")

def refund(request):
    return render(request,"refund.html")




def products(request,product_cat=None):
    all_products = Product.objects.all()
    if product_cat:
        all_products = Product.objects.filter(quote_type=product_cat)

    # if request.method =="POST":
    #     search = request.POST.get("search")
    #     all_products = Product.objects.filter(Q(name__icontains=search) | Q(desp__icontains=search))

    paginator = Paginator(all_products,9)
    page = request.GET.get("page")
    all_products = paginator.get_page(page)


    context = {
        "product":all_products
    }
    return render(request, "products_2.html",context)

def product_detail(request,id):

    product = get_object_or_404(Product,id=id)
    discount_percentage = 0
    if product.is_discount:
        discount_percentage = round(100 - (int(product.discount_price) / int(product.price)) * 100)

    other_size = Product.objects.filter(name=product.name)


    context = {
        "product":product,
        "discount_percentage":discount_percentage,
        "other_size":other_size
    }
    return render(request,"product.html",context)

def about_us(request):

    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("cname")
        email = request.POST.get("cemail")
        phone_no = request.POST.get("cphone")
        subject = request.POST.get("csubject")
        message = request.POST.get("cmessage")

        try:
            CustomerForm.objects.create(
                name = name,
                email = email,
                phone_no = int(phone_no),
                subject = subject,
                message = message
            )
            messages.success(request,"Your message is submitted")
            return redirect("contact")
        except Exception as e:
            messages.error(request,"there is problem with your info, Please check and try again")
            print(e)

    return render(request,"contact.html")


def order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_paid=True,is_shipped=False).order_by("ordered_date")


        paginator = Paginator(orders,10)
        page = request.GET.get("page")
        orders = paginator.get_page(page)
        context = {
            "orders":orders
        }

        return render(request,"order.html",context)
    else:
        return redirect("home")

def order_details(request,pk):
    if request.user.is_authenticated:
        order = Order.objects.get(pk=pk)
        products = OrderItems.objects.filter(order=order)

        context = {
            "products":products,
            "order":order
        }

        return render(request,"order_details.html",context)
    else:
        return redirect("home")


def your_order(request):
    if request.user.is_authenticated:
        try:
            orders = Order.objects.filter(user=request.user)
            context = {
               "orders":orders,
            }
            return render(request,"order.html",context)

        except Exception as e:
            return render(request,"order.html",{"no_order":"Your have no order on queue"})
    return redirect("home")

def update_shipped(request,pk):
    order = Order.objects.get(pk=pk)
    order.is_shipped =True
    order.save()
    messages.success(request,"Order is shipped and updated in model")
    return redirect("orders")
