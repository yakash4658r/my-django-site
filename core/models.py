from django.db import models
import uuid
# Create your models here.
class Product(models.Model):
    small = "small"
    medium = "medium"
    large = "large"
    SIZE_CHOICE = [
        (small,"Small"),
        (medium,"Medium"),
        (large,"Large"),
    ]

    product_cat = [
        ("english_quote","English Quote"),
        ("tamil_quote","Tamil Quote"),
    ]

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255)
    desp = models.TextField()
    size = models.CharField(max_length=255,choices=SIZE_CHOICE,default="small")
    price = models.DecimalField(max_digits=8,decimal_places=0)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=8,decimal_places=0,null=True,blank=True)
    no_of_sales = models.IntegerField(default=0)
    quote_type = models.CharField(choices=product_cat,max_length=255,default="english_quote")
    image_1 = models.ImageField(upload_to="product_images/",default="default_product.jpg")
    image_2 = models.ImageField(upload_to="product_images/",null=True,blank=True)
    image_3 = models.ImageField(upload_to="product_images/",null=True,blank=True)
    image_4 = models.ImageField(upload_to="product_images/",null=True,blank=True)



    def __str__(self):
        return self.name

class CustomerForm(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.BigIntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name