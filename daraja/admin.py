from django.contrib import admin

from daraja.models import Transaction
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'status', 'is_confirmed', 'receipt_no',)
    list_filter = ('receipt_no', 'status')
    search_fields = ('receipt_no', 'checkout_request_id', )
