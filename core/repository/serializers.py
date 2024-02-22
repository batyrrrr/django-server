from .models import Repository
from core.user.models import User
from rest_framework import serializers
from core.user.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer


class RepositorySerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="public_id"
    )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(public_id=rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep

    def validate_author(self, value):
        if (
            self.context["request"].user.is_superuser
            or self.context["request"].user == value
        ):
            return value
        raise ValidationError("Unauthorized")

    class Meta:
        model = Repository
        fields = [
            "id",
            "title",
            "edited",
            "author",
            "created_at",
            "updated_at",
            "description",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
