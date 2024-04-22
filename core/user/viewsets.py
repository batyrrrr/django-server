from core.user.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import IsSuperuserOrIsCurrentUser
from core.user.serializers import PasswordUpdateSerializer, UpdateIsActiveSerializer


class UserViewSet(AbstractViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsSuperuserOrIsCurrentUser]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        request = self.request
        if request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(public_id=request.user.public_id)

    def get_object(self):
        instance = User.objects.get_object_by_public_id(self.kwargs.get("pk"))
        self.check_object_permissions(self.request, instance)
        return instance

    @action(detail=True, methods=["patch"], url_path="activate-user")
    def update_is_active(self, request, pk=None):
        user = self.get_object()
        serializer = UpdateIsActiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response({"detail": "User account status updated successfully."})

    @action(detail=True, methods=["patch"], url_path="update-password")
    def update_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response({"detail": "Password updated successfully."})
