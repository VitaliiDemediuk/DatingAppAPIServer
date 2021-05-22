from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, *args, **kwargs):
        return request.method in permissions.SAFE_METHODS or \
               IsAdminUser().has_permission(request, *args, **kwargs)

    def has_object_permission(self, request,  *args, **kwargs):
        return request.method in permissions.SAFE_METHODS or \
               IsAdminUser().has_object_permission(request, *args, **kwargs)
