from django.contrib import admin
from step3.models import FirstGuarantor, SecondGuarantor

# Register your models here.
@admin.register(FirstGuarantor)
class FirstGuarantorAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'phone_number', 'relationship',)
    list_filter = ('phone_number', 'relationship', )

@admin.register(SecondGuarantor)
class SecondGuarantorAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'phone_number', 'relationship',)
    list_filter = ('phone_number', 'relationship',)
