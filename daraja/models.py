import uuid
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
STATUS = ((1, "Pending"), (0, "Complete"))

User = get_user_model()

class Transaction(models.Model):
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"

class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.IntegerField(null=False, blank=False, default=0)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return f"{self.transaction_no}"

    class Meta:
        db_table = "savings"
        verbose_name = "Savings"
        verbose_name_plural = "Savings"
        
