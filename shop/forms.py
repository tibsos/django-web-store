# shop/forms.py

from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="ФИО")
    address = forms.CharField(widget=forms.Textarea, label="Адрес доставки")
    phone_number = forms.CharField(max_length=15, label="Телефон")
    email = forms.EmailField(label="Электронная почта")
