# permissions.py
from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object or a staff user to edit or delete it.
    """
    pass


'''
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

'''