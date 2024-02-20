from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """Validating the request data before obtaining the refresh and access token from the inherited class."""
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Update last timestamps of the User
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
