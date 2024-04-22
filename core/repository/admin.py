from django.contrib import admin
from .models import Repository, Category


# Register your models here.
@admin.register(Category)
class CustomCategotyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["created_at", "updated_at"]


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
