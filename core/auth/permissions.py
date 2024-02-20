from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            author = str(request.user.public_id)
            parsed_author = author.replace("-", "")
            return bool(
                request.user.is_superuser or parsed_author == request.data.get("author")
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            print(request.user)
            return bool(request.user.is_superuser or request.user == obj.author)
        return False


# class IsAuthorOrOwnerOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return request.user and request.user.is_authenticated
#         elif request.method == "POST":
#             return request.user.is_superuser or request.user == request.data.get("author")
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         elif request.method in ["PUT", "PATCH", "DELETE"]:
#             return request.user.is_superuser or obj.author == request.user
#         return False
