from rest_framework.permissions import BasePermission


class CommentsPermissions(BasePermission):
    """
    Права доступа для комментариев
    GET, POST - все
    PUT, PUTCH, - только автор
    DELETE - автор и superuser
    """
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        if request.user.is_authenticated:
            if view.action in ('update', 'partial_update'):
                return request.user == obj.author
            if view.action == 'destroy':
                return request.user == obj.author or request.user.is_superuser
        return False
