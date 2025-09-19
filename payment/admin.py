from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)


class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]
    list_display = ['user',"is_paid","is_shipped","ordered_date"]

    readonly_fields = ["ordered_date","payment_id","signature","order_id"]
    search_fields = ["is_paid"]

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItems
    list_display = ['order',"product","product_price"]



admin.site.unregister(Order)
admin.site.register(Order,OrderAdmin)

admin.site.unregister(OrderItems)
admin.site.register(OrderItems,OrderItemAdmin)
