from django import forms
from .models import ShippingAddress
class ShippingAddressForm(forms.ModelForm):
    class Meta:

        model = ShippingAddress
        fields = "__all__"
        labels = {
            "phone_no":"Enter the Whatsapp Number",
        }

        widgets = {

            "email":forms.EmailInput,
        }
