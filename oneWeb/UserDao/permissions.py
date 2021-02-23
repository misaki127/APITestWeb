from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    #自定义权限

    def has_object_permission(self, request, view, obj):
        #允许GET，HEAD或OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
