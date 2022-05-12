from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission): # I create a new custom permission because there is no default to make the GET available to anyone(readonly) and the create,modify,delete only for the admin
    def has_permission(self, request, view):
        if request.method == 'GET': # or if request.method in permissions.SAFE_METHODS
            return True 
        else:
            return bool(request.user and request.user.is_staff) # return True if the requester is a user and is also part of the staff
