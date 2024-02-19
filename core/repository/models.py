from django.db import models
from core.abstract.models import AbstractModel


class Repository(AbstractModel):
    title = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    description = models.TextField(max_length=500)
    file = models.FileField(null=True, blank=True, upload_to="repositories/", max_length=500)
    author = models.ForeignKey(
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
