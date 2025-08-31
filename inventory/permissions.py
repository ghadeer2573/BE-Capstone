from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Owner or staff can modify
        return getattr(obj, 'owner', None) == request.user or request.user.is_staff
