from django.db import models
import secrets
from .wavePayment import FlutterWave



class CurrencyChoices(models.TextChoices):
    """Choices for the supported currencies."""
    NGN = 'NGN', 'Nigerian Naira'
    USD = 'USD', 'US Dollar'
    GBP = 'GBP', 'British Pound'



class Payment(models.Model):
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=3,  
        choices=CurrencyChoices.choices,  
        default=CurrencyChoices.NGN,  # Default to NGN
    )
    tx_ref = models.CharField(max_length=200, unique=True)
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
            while Payment.objects.filter(tx_ref=tx_ref).exists():
                tx_ref = secrets.token_urlsafe(50)
            self.tx_ref = tx_ref

        
        super().save(*args, **kwargs)