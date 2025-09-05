from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    method_map = {
        'GET': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }
    app_label_map = {
        'asset': 'asset',
        'company': 'company',
        'floor': 'floor',
        'branch': 'branch',
        'building': 'building',
        'room': 'room',
        'user': 'user',
        'role': 'role',
        'permissions': 'permissions',
    }

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        try:
            user_role = user.role
            user_permissions = user_role.permissions.values_list('codename', flat=True)

        except AttributeError:
            return False

        model = None

        try:
            queryset = view.get_queryset()
            if queryset:
                model = queryset.model
                print(model)
        except Exception:
            model = None

        if model is None:
            try:
                serializer_class = view.get_serializer_class()
                model = serializer_class.Meta.model
            except Exception:
                model = None

        if model is None:
            return False

        action = self.method_map.get(request.method)

        if action is None:
            return False

        model_name = model._meta.model_name.lower()

        app_label = self.app_label_map.get(model_name, model._meta.app_label.lower())

        perm_codename_full = f"{app_label}.{action}_{model_name}"
        perm_codename_simple = f"{action}_{model_name}"

        return perm_codename_full in user_permissions or perm_codename_simple in user_permissions
