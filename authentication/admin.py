from django.contrib import admin

from authentication.models import User

admin.site.site_header = "CHAMA YETU ADMIN"

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','firstname', 'lastname', 'middlename', 'is_verified', 'phone_number', 'is_superuser')
    list_display_links = ('firstname', 'lastname', 'middlename', 'phone_number', 'is_superuser')

    search_fields = ('id', 'firstname', 'lastname', 'middlename', 'phone_number', 'is_superuser')

    list_per_page = 25

    ordering = ['id']
