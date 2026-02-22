from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # anyone can read (GET), only the author can write (PUT, DELETE)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user