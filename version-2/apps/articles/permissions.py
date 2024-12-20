from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdminUser(BasePermission):
    """
    Custom permission to allow only admin users to perform certain actions.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return request.user.is_authenticated and request.user.role == 'admin'


class IsJournalist(permissions.BasePermission):
    """
    Custom permission to only allow journalists to create and update their articles.
    """
    def has_permission(self, request, view):
        # Allow journalists to create articles
        if view.action == 'create':
            return request.user.role == 'journalist'
        return True  # Let other actions pass

    def has_object_permission(self, request, view, obj):
        # Allow journalists to update or delete their own articles
        if view.action in ['update', 'partial_update', 'destroy']:
            # Ensure the user is the author of the article
            if request.user.role == 'journalist' and obj.author == request.user:
                # Check if the article is in "published" state
                if obj.status == 'published':
                    return False  # Can't update or delete published articles
                return True
        return False

class IsEditor(permissions.BasePermission):
    """
    Custom permission to only allow editors to view and change the status of articles.
    """
    def has_permission(self, request, view):
        # Allow editors to change article status
        if view.action in ['update', 'partial_update']:
            return request.user.role == 'editor'
        return True  # Let other actions pass
    
    def has_object_permission(self, request, view, obj):
        # Editors can update status but not delete or modify the article content
        if view.action in ['update', 'partial_update']:
            if request.user.role == 'editor':
                # Editors can change status but can't delete the article
                return True
        return False
    
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
        if request.user.role == 'journalist':
            return True  # Journalists can access all actions for their own articles.

        if request.user.role == 'editor':
            # Editors can only view or update status.
            return view.action in ['list', 'retrieve', 'change_status']

        return False

    def has_object_permission(self, request, view, obj):
        """
        Define object-level permissions:
        - Journalists: Can modify their own articles, with restrictions.
        - Editors: Can view all articles and update their status.
        """
        if request.user.role == 'journalist':
            # Journalists can only modify their own articles.
            return obj.author == request.user

        if request.user.role == 'editor':
            # Editors can view and update status but not modify article content.
            return view.action in ['retrieve', 'change_status']

        return False
