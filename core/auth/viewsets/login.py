from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.auth.serializers.login import LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class LoginViewSet(viewsets.ViewSet):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """Return the refresh and access token after being validated the request data by the serializer."""
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as error:
            raise InvalidToken(error.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
