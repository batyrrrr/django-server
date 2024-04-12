import re
from django.conf import settings
from core.user.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from core.user.serializers import UserSerializer
from core.utils.validator import validate_password


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        min_length=8,
        max_length=255,
        write_only=True,
        required=True,
    )
    is_superuser = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=False)

    def validate_password(self, value):
        """Validate password to ensure it meets requirements."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Save the user object after being validated by the User Manager."""
        self.send_registration_email(validated_data.get("email"))
        return User.objects.create_user(**validated_data)

    def send_registration_email(self, email):
        """Send a registration email to the user."""
        subject = "Welcome to VCLab!"
        message = "You have successfully registered to VCLab. Please wait for the admin to approve your account."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_superuser",
            "is_active",
        ]
