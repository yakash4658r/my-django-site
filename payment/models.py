import uuid

from django.db import models
from django.contrib.auth.models import User
from core.models import Product
# Create your models here.
class ShippingAddress(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.RESTRICT)
    address = models.OneToOneField(ShippingAddress,on_delete=models.RESTRICT)
    order_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    amount_paid = models.PositiveBigIntegerField(null=True,blank=True)
    payment_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    signature = models.CharField(max_length=255,null=True,blank=True,editable=False)
    is_shipped = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"



class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.RESTRICT)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)

    product_name = models.CharField(max_length=255)
    product_size = models.CharField(max_length=255)
    product_price = models.IntegerField()
    product_qty = models.IntegerField()


