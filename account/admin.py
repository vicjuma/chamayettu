from django.contrib import admin

from account.models import PersonalInfoStepOne, PersonalInfoStepTwo, FirstGuarantor, SecondGuarantor, ContibutionFrequency
# Register your models here.
@admin.register(PersonalInfoStepOne)
class PersonalInfoStepOneAdmin(admin.ModelAdmin):
    list_display = ('user', 'lastname', 'idnumber', 'dateofbirth', 'gender', 'status', 'education')
    list_filter = ('gender', 'education')

@admin.register(PersonalInfoStepTwo)
class PersonalInfoStepTwo(admin.ModelAdmin):
    list_display = ('user', 'email', 'employment', 'income')
    list_filter = ('email', 'income',)

@admin.register(FirstGuarantor)
class FirstGuarantorAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'phone_number', 'relationship',)
    list_filter = ('phone_number', 'relationship', )

@admin.register(SecondGuarantor)
class SecondGuarantorAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'phone_number', 'relationship',)
    list_filter = ('phone_number', 'relationship',)

@admin.register(ContibutionFrequency)
class ContibutionFrequencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'frequency',)
    list_filter = ('frequency',)