# core/permissions.py

from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsVolunteer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'VOLUNTEER'

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CLIENT'
