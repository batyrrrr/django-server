from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import (
    permissions,
    viewsets,
    status,
)


class LogoutViewSet(viewsets.ViewSet):
    http_method_names = ["post"]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Generated token will automatically be available in blacklisted."""
        try:
            refresh = request.data.get("refresh_token")
            token = RefreshToken(refresh)
            token.blacklist()
            return Response("Logout Successfully!", status=status.HTTP_200_OK)
        except TokenError as error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
