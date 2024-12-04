from django.contrib import admin
from .models import PaystackPayment


@admin.register(PaystackPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'amount', 'currency', 'tx_ref', 'email', 'verified', 'created_at')
    list_filter = ('currency', 'verified', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'email', 'tx_ref')
    readonly_fields = ('tx_ref', 'verified', 'created_at','customer_phone', 'amount','currency','email')
