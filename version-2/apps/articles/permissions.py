from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdminUser(BasePermission):
    """
    Custom permission to allow only admin users to perform certain actions.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return request.user.is_authenticated and request.user.role == 'admin'

  
class IsJournalistOrEditor(BasePermission):
    """
    Custom permission to allow actions based on roles.
    """

    def has_permission(self, request, view):
        """
        Allow actions based on user role:
        - Journalists: Can create, update, delete, and view their own articles.
        - Editors: Can view all articles and update their status, but cannot create articles.
        """
        # Journalists can access their own articles but cannot change the status
        if request.user.role == 'journalist':
            if view.action in ['change_status']:
                return False
            return True

        # Editors can do everything except create articles
        if request.user.role == 'editor':
            return view.action in ['list', 'retrieve', 'change_status', 'partial_update']

        return False

    def has_object_permission(self, request, view, obj):
        """
        Define object-level permissions:
        - Journalists: Can modify their own articles, with restrictions.
        - Editors: Can view all articles and update their status.
        """
        if request.user.role == 'journalist':
            # Journalists can only modify their own articles but cannot change the status
            if view.action == 'change_status':
                return False
            return obj.author == request.user

        if request.user.role == 'editor':
            # Editors can view and update status but not modify article content.
            return view.action in ['retrieve', 'change_status', 'partial_update']

        return False
