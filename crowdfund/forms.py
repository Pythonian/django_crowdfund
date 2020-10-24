from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'country']


# from .models import PaystackInfo

# class PaystackInfoForm(forms.ModelForm):
#     class Meta:
#         model = PaystackInfo
#         fields = '__all__'