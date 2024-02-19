from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            user_public_id = str(request.user.public_id).replace("-", "")
            author_public_id = request.data.get("author").replace("-", "")
            return bool(request.user.is_superuser or user_public_id == author_public_id)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            return bool(request.user.is_superuser or obj.author == request.user)
        return False
