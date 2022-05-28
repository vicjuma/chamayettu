import uuid
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from account.models import Chama

# Create your models here.
STATUS = ((1, "Pending"), (0, "Complete"))

User = get_user_model()

class Transaction(models.Model):
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, null=True, blank=True)
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

    @property
    def total_amount(self):
        # calculate total amount of each user
        total = 0
        for savings in self.user.savings_set.all():
            total += savings.amount
        return total

    class Meta:
        db_table = "savings"
        verbose_name = "Savings"
        verbose_name_plural = "Savings"

class TotalAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.Case)
    total = models.IntegerField(default=0)
    deductions = models.IntegerField(default=0)

    @property
    def value(self):
        return self.total - self.deductions

    class Meta:
        db_table = 'total_amount'
        verbose_name = 'Total Amount'
        

        
