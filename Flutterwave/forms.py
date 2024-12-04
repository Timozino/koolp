from django import forms



class PaymentForm(forms.ModelForm):
    
    class Meta:
        from .models import Payment
        model = Payment
        fields = ['customer_name', 'customer_phone', 'amount', 'currency', 'email']