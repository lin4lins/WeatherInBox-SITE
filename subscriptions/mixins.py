from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.COOKIES.get('jwt_token'):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
