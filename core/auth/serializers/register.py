from core.user.models import User
from rest_framework import serializers
from core.user.serializers import UserSerializer


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        min_length=8, max_length=255, write_only=True, required=True
    )

    def create(self, validated_data):
        """Save the user object after being validated by the User Manager."""
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        ]
