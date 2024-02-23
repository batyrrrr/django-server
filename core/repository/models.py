from django.db import models
from core.abstract.models import AbstractModel


class Category(AbstractModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Repository(AbstractModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="category",
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        to="core_user.User",
        on_delete=models.RESTRICT,
        related_name="user_repository",
    )

    def __str__(self):
        return f"{self.title}-{self.author}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"
