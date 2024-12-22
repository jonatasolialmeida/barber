from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permissão que permite acesso apenas ao dono ou para leitura."""

    def has_object_permission(self, request, view, obj):
        # Permite acesso total para o dono, ou leitura para outros
        if request.user.is_owner:
            return True
        return request.method in permissions.SAFE_METHODS

class IsClient(permissions.BasePermission):
    """Permissão que permite acesso apenas aos clientes."""

    def has_permission(self, request, view):
        # Permite acesso apenas a clientes
        return request.user.is_authenticated and request.user.is_client

class IsProfessional(permissions.BasePermission):
    """Permissão que permite acesso apenas aos profissionais."""

    def has_permission(self, request, view):
        # Permite acesso apenas a profissionais
        return request.user.is_authenticated and request.user.is_professional

class IsAdminOrOwner(permissions.BasePermission):
    """Permissão que permite acesso apenas ao administrador ou ao proprietário do estabelecimento."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_owner or request.user.is_staff)

class IsOwner(permissions.BasePermission):
    """Permissão que permite acesso apenas ao proprietário."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_owner
