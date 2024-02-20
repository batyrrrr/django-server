from rest_framework import filters
from rest_framework import viewsets


class AbstractViewSet(viewsets.ModelViewSet):
    """All ViewSets will have the same ordering system."""

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at"]
