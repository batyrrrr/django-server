import uuid
from django.db import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class AbstractManager(models.Manager):
    """Inherited from models.Manager in defining custom manager."""

    def get_object_by_public_id(self, public_id):
        try:
            return self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractModel(models.Model):
    """db_index = True | for faster lookups"""
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AbstractManager()

    class Meta:
        """Serve as a blueprint for other class model. """
        abstract = True