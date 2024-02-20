from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.auth.serializers.register import RegisterSerializer


class RegisterViewSet(viewsets.ViewSet):
    http_method_names = ["post"]
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        The only required fields are the following, username, email and password the rest are optional.
        First it check the request data if valid by serializing then save.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Registered Successfully", status=status.HTTP_201_CREATED)
