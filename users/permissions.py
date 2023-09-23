from rest_framework import permissions


class IsStaffOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().owner
