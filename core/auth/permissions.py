from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOrIsCurrentUser(BasePermission):
    """
    Only Superuser or the user itself can perform (CRUD) the user data.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(obj == request.user or request.user.is_superuser)


class IsSuperuser(BasePermission):
    """
    Only Superuser can register a new user.
    """

    def has_permission(self, request, view):
        if request.method in ["POST"]:
            return bool(request.user and request.user.is_superuser)
        return False


class IsSuperuserOrReadOnly(BasePermission):
    """
    Only allow superusers to perform POST, PATCH, DELETE for repositories matter.
    Authenticated users can perform GET.
    """

    def has_permission(self, request, view):
        # Allow GET requests for all authenticated users
        if request.method in ["GET"]:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_superuser)
