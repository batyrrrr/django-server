from rest_framework import filters
from rest_framework import viewsets


class AbstractViewSets(viewsets.ModelViewSet):
    """All ViewSets will have the same ordering system."""
    filter_backends =[filters.OrderingFilter]
    ordering_fields = ["updated", "created"]
    ordering = ["-updated"]