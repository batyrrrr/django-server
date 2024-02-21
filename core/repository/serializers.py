from .models import Repository
from core.user.models import User
from rest_framework import serializers
from core.user.serializers import UserSerializer
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
