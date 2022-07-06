from django.contrib import admin

from authentication.models import User

admin.site.site_header = "CHAMA YETU ADMIN"

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_verified', 'phone_number', 'is_superuser','email',)
    list_display_links = ('phone_number', 'is_superuser', 'email',)
    list_filter = ('phone_number', 'is_superuser', 'email',)
    search_fields = ('id', 'phone_number', 'is_superuser', 'email',)
    list_per_page = 25
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {
            "fields": (
                'phone_number',
            ),
        }),
        ("Permissions", {
            "fields": (
                'is_verified', 'is_staff', 'is_active', 'is_superuser'
            ),
        }),
        ("Personal", {
            "fields": (
                'email',
            ),
        }),
    )
    
