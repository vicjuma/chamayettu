from django.contrib import admin
from step1.models import PersonalInfoStepOne

# Register your models here.
@admin.register(PersonalInfoStepOne)
class PersonalInfoStepOneAdmin(admin.ModelAdmin):
    list_display = ('user', 'lastname', 'idnumber', 'dateofbirth', 'gender', 'status', 'education')
    list_filter = ('gender', 'education')
