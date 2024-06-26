from .models import Repository
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RepositorySerializer
from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import IsSuperuserOrReadOnly


class RepositoryViewSet(AbstractViewSet):
    permission_classes = [IsSuperuserOrReadOnly]
    serializer_class = RepositorySerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """fetch all repositories"""
        return Repository.objects.prefetch_related("creator").all()

    def get_object(self):
        """Fetch the repository detail.
        In Django, when you define a URL pattern with a path converter,
        such as <int:pk> or <slug:pk>, the captured value is stored in the kwargs attribute of the view class.
        """
        obj = Repository.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        """
        Rewriting the update function to ensure the edited field is set to True when
        modifying the recipe and only allow the author of the recipe or superuser only.
        """
        instance = self.get_object()
        if not instance.edited:
            instance.edited = True
            instance.save()
        return super().update(request, *args, **kwargs)
