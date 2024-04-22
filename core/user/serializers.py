from .models import User
from django.conf import settings
from core.utils import validator
from django.core.mail import send_mail
from rest_framework import serializers
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

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class UpdateIsActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)

    def update(self, instance, validated_data):
        """Update the user instance."""
        is_active_updated = validated_data.get("is_active")
        if is_active_updated != instance.is_active:
            instance.is_active = is_active_updated
            instance.save()

            # Send an Email
            self.send_email_activation_status(instance.email, is_active_updated)
        return instance

    def send_email_activation_status(self, email, is_active):
        """Send email to user to notify them of their account status."""
        if is_active:
            message = (
                "Your account has been activated successfully and you can now login."
            )
        else:
            message = "Your account has been deactivated. Please contact the admin for more information."
        subject = "Account Activation Status"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8,
        max_length=255,
        write_only=True,
        required=True,
    )

    def validate_password(self, value):
        """Validate password to ensure it meets requirements."""
        validator.validate_password(value)
        return value

    def update(self, instance, validated_data):
        """Update the user password."""
        instance.set_password(validated_data.get("password"))
        instance.save()
        self.send_email_update_password(
            instance.email,
            message=f"Please keep your password safe.{validated_data.get('password')}",
        )
        return instance

    def send_email_update_password(self, email, message):
        """Send email to user to notify them of their password update."""
        message = f"Your password has been updated successfully. {message}"
        subject = "Password Update"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
