from rest_framework import permissioms

class IsOwner(permissions.BasePermission):
    ''' Custom permission to only allow owners of an object to access it. 
        Assumes the model instance has an `user` attribute.''' 
    
    def has_object_permission(self, request, view, obj):
        ''' Read permissions are allowed to any request,
            so we'll always allow GET, HEAD or OPTIONS requests'''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user 