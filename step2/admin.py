from django.contrib import admin
from step2.models import PersonalInfoStepTwo

# Register your models here.
@admin.register(PersonalInfoStepTwo)
class PersonalInfoStepTwo(admin.ModelAdmin):
    list_display = ('user', 'email', 'employment', 'income')
    list_filter = ('email', 'income',)
