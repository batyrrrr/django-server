from core.user.models import User
from .serializers import UserSerializer
from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import IsAuthorOrOwnerOrAdmin


class UserViewSet(AbstractViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthorOrOwnerOrAdmin]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        """Return a user information."""
        return User.objects.filter(public_id=self.request.user.public_id)
