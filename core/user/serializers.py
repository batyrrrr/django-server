from .models import User
from core.abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
    class Meta:
        """List of all fields that will be included in request or a response."""

        model = User
        fields = [
            "id",
            "email",
            "username",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_active"]
