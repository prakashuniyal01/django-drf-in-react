from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission for Admins who can do all CRUD operations.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsJournalist(permissions.BasePermission):
    """
    Permission for Journalists to allow CRUD on their own articles.
    """
    def has_permission(self, request, view):
        # Only allow CRUD if user is a journalist
        return request.user.role == 'journalist'

    def has_object_permission(self, request, view, obj):
        # Journalists can only access their own articles
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsEditor(permissions.BasePermission):
    """
    Permission for Editors to change the status of articles but not create, read, or delete them.
    """
    def has_permission(self, request, view):
        return request.user.role == 'editor'

    def has_object_permission(self, request, view, obj):
        # Editors can only update the status of articles
        if request.method == 'PATCH':
            if 'status' in request.data:
                return True
        return False


class IsPublishedOrAuthenticated(permissions.BasePermission):
    """
    Read-only permission for users to view published articles.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET requests (read)
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET requests (read)
            return obj.status == 'published'  # Only published articles can be read
        return False
