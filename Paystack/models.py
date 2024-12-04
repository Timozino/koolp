from django.db import models
import secrets


class CurrencyChoices(models.TextChoices):
    """Choices for the supported currencies."""
    NGN = 'NGN', 'Nigerian Naira'
    USD = 'USD', 'US Dollar'
    GBP = 'GBP', 'British Pound'
    
    


class PaystackPayment(models.Model):
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=3,  
        choices=CurrencyChoices.choices,  
        default=CurrencyChoices.NGN,  # Default to NGN
    )
    tx_ref = models.CharField(max_length=200, unique=True, default="1")
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.pk} - {self.customer_name or "Anonymous"} - {self.tx_ref}'

    
    def save(self, *args, **kwargs):
        if not self.tx_ref:
            tx_ref = secrets.token_urlsafe(50)
            while PaystackPayment.objects.filter(tx_ref=tx_ref).exists():
                tx_ref = secrets.token_urlsafe(50)
            self.tx_ref = tx_ref

        
        super().save(*args, **kwargs)





# class Payment(models.Model):
#     customer_name = models.CharField(max_length=255, null=True, blank=True)
#     customer_phone = models.CharField(max_length=15, null=True, blank=True)
#     amount = models.PositiveIntegerField()
#     currency = models.CharField(
#         max_length=3,  
#         choices=CurrencyChoices.choices,  
#         default=CurrencyChoices.NGN,  # Default to NGN
#     )
#     ref = models.CharField(max_length=200)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-date_created']

#     def __str__(self) -> str:
#         return f"Payment: {self.amount} {self.currency}"
    
#     def save(self, *args, **kwargs):
#         while not self.ref:
#             self.ref = secrets.token_hex(50)
#             object_with_same_ref = Payment.objects.filter(ref=self.ref)
#             if object_with_same_ref.exists():
#                 self.ref = f"{self.ref}-{self.customer_phone}"
                
#         super().save(*args, **kwargs)
        
        
#     def amount_value(self) -> int:
#         return self.amount*100
                
        
