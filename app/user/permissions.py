from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAdminUserOrIsGet(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or (request.method == 'GET')