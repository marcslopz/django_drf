from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions


def add_permission_to_add_model(model_class, group):
    model_content_type = ContentType.objects.get_for_model(model_class)
    permission_to_be_added = \
        Permission.objects.filter(content_type=model_content_type, codename__startswith='add').first()
    if permission_to_be_added:
        group.permissions.add(permission_to_be_added)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an blog post instance to edit it.
    """
    @staticmethod
    def _is_an_author(user, obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return user.groups.filter(permissions__codename__startswith='add', permissions__content_type=obj_type).exists()

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the author can change/delete object
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return obj.author == request.user
        elif request.method == 'POST':
            return self._is_an_author(request.user, obj)
        else:
            return False
