from rest_framework import permissions

class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for read-only access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check for ownership/participation (the write access)
        # This checks if the currently logged-in user is one of the participants
        return request.user in obj.participants.all()

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow access ONLY if the user is logged in (authenticated)
        return request.user.is_authenticated
