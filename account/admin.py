from django.contrib import admin

from account.models import Chama, ContibutionFrequency
# Register your models here.

@admin.register(ContibutionFrequency)
class ContibutionFrequencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'frequency',)
    list_filter = ('frequency',)

admin.site.register(Chama)