from .models import Repository
from rest_framework import status
from rest_framework.response import Response
from .serializers import RepositorySerializer
from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import IsAuthenticatedOrAdmin
# from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RepositoryViewSet(AbstractViewSet):
    permission_classes = [IsAuthenticatedOrAdmin]
    serializer_class = RepositorySerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Repository.objects.prefetch_related("author").all()
