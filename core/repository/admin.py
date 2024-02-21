from .models import Repository
from django.contrib import admin


# Register your models here.
@admin.register(Repository)
class CustomRepositoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "edited",
        "description",
    ]
    list_filter = ["author"]
    readonly_fields = ["edited", "created_at", "updated_at"]
