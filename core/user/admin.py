from . models import User
from django.contrib import admin


# Register your models here.
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "public_id",
        "username",
        "first_name",
        "last_name",
        "email",
        "created_at",
        "updated_at",
        "is_active",
        "is_superuser",
    ]
    list_filter = [
        "is_active",
        "is_superuser"
    ]
