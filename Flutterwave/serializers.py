from rest_framework import serializers
from .models import Payment, CurrencyChoices

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the Payment model."""

    class Meta:
        model = Payment
        fields = ['id', 'customer_name', 'customer_phone', 'amount', 'currency', 'tx_ref', 'email', 'verified', 'created_at']

    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive integer.")
        return value

    def validate_currency(self, value):
        """Validate the currency field."""
        if value not in CurrencyChoices.values:
            raise serializers.ValidationError("Invalid currency choice.")
        return value
