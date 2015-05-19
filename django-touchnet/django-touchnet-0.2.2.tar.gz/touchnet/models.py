from django.db import models

class PostbackLog(models.Model):
    remote_ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=2048)
    
    PAYMENT_CANCELLED = 'cancelled'
    PAYMENT_SUCCESS = 'success'
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_SUCCESS, 'Success'),
        (PAYMENT_CANCELLED, 'Cancelled')
    )
    payment_status = models.CharField(max_length=9, choices=PAYMENT_STATUS_CHOICES, blank=True)
    transaction_id = models.CharField(max_length=256, blank=True)
    payment_amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    
    processed = models.BooleanField()
    result = models.CharField(max_length=2048)
    post = models.CharField(max_length=2048)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']