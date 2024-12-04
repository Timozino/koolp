from django import forms
from .models import PaystackPayment  # Move this import to the top


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaystackPayment
        fields = ['customer_name', 'customer_phone', 'amount', 'currency', 'email']
