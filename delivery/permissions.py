from rest_framework import permissions


class DeleteUserPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.user.has_perm('delivery.delete_user'):
            return True
        return False
