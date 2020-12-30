from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'country']


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Name'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Subject'}), required=True)
    from_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Subject'}), required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Your message'}), required=True)
