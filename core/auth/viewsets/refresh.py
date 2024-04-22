from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Return a brandnew access token based on the current refresh token generated from login endpoint."""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as error:
            raise InvalidToken(error.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
