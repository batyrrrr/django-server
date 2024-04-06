from .models import User
from rest_framework import serializers
from core.utils.validator import validate_password
from core.abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
    class Meta:
        """List of all fields that will be included in request or a response."""

        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "fullname",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_active", "repo_name"]


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8,
        max_length=255,
        write_only=True,
        required=True,
    )

    def validate_password(self, value):
        """Validate password to ensure it meets requirements."""
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        """Update the user password."""
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
