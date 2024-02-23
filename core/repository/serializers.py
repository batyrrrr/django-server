from core.user.models import User
from rest_framework import serializers
from .models import Repository, Category
from core.user.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer


class CategorySerializer(AbstractSerializer):
    class Meta:
        model = Category
        fields = ["name", "created_at", "updated_at"]


class RepositorySerializer(AbstractSerializer):
    creator = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="public_id"
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        creator = User.objects.get_object_by_public_id(
            public_id=representation["creator"]
        )
        representation["creator"] = UserSerializer(creator).data
        representation["category"] = instance.category.name
        return representation

    def validate_creator(self, value):
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
            "creator",
            "category",
            "is_public",
            "created_at",
            "updated_at",
            "description",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
