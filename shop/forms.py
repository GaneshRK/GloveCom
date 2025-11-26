from django import forms
from .models import Order
class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address','city','postal_code']
