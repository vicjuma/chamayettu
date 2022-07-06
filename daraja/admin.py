from django.contrib import admin
from django.contrib.auth import get_user_model

from daraja.models import Savings, Transaction



User = get_user_model()
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'status', 'is_confirmed', 'receipt_no',)
    list_filter = ('receipt_no', 'status')
    search_fields = ('receipt_no', 'checkout_request_id', )

class SavingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'amount', 'is_confirmed', 'receipt_no',]
    list_filter = ('receipt_no', 'is_confirmed',)
    search_fields = ('receipt_no', 'checkout_request_id', )

    # set default filter to is_confirmed = True
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_confirmed=True)

    #display user firstname and lastname instead of id
    def user(self, obj):
        return obj.user.get_full_name()


admin.site.register(Savings, SavingsAdmin)