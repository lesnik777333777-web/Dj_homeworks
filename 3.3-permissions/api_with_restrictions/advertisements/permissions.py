from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее читать всем, а изменять/удалять только автору или администратору.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS любому пользователю
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить изменение/удаление только автору или администратору (is_staff)
        return obj.creator == request.user or (request.user.is_authenticated and request.user.is_staff)