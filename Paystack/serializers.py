from rest_framework import serializers
from .models import PaystackPayment


class PaystckPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaystackPayment
        fields = [
            'id', 
            'customer_name', 
            'customer_phone', 
            'amount', 
            'currency', 
            'tx_ref', 
            'email', 
            'verified', 
            'created_at'
        ]
        read_only_fields = ['id', 'tx_ref', 'verified', 'created_at','customer_phone', 'amount','currency','email']

