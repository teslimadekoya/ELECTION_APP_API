from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_authenticated  and request.user.role == 'admin'
    
class IsVoter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff and request.user.role == 'voter'
    
class IsBoth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'voter' or request.user.role == 'admin') 