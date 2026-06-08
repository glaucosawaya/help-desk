from django.http import Http404


class AdminOnlyMixin:

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        if request.user.role != "ADMIN":
            raise Http404()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )