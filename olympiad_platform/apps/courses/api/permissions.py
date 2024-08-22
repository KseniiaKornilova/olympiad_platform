from rest_framework.permissions import BasePermission


class IsEnrolledOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(id=request.user.id).exists() or request.user.is_staff
