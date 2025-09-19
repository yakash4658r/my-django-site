from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("Terms_&_Conditions", terms, name="terms"),
    path("privacy_policy", policy, name="privacy_policy"),
    path("refund/", refund, name="refund"),
    path("products/", products, name="products"),
    path("products/<product_cat>", products, name="products"),
    path("product/<id>", product_detail, name="product"),
    path("about_us/", about_us, name="about"),
    path("contact/", contact, name="contact"),
    path("orders/", order, name="orders"),
    path("order_details/<pk>", order_details, name="order_details"),
    path("your_orders/", your_order, name="your_orders"),
    path("update_shipped/<pk>", update_shipped, name="update_shipped"),
    path("shipping_page/", shipping_page, name="shipping_page"),
]