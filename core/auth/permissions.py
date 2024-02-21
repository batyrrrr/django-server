from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            return bool(request.user and request.user.is_authenticated)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            return bool(
                (request.user.is_authenticated and request.user == obj.author)
                or request.user.is_superuser
            )
        return False
