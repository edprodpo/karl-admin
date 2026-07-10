from django.shortcuts import render


class AdminMixin:
    forbidden_template = 'exceptions.html'
    title_page = 'Доступ запрещён'
    status_code = 403
    detail = 'У вас нет прав для просмотра этой страницы.'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not user.is_superuser:
            return render(
                request=request,
                template_name=self.forbidden_template,
                context={
                    'title': self.title_page,
                    'status_code': self.status_code,
                    'detail': self.detail,
                },
                status=403,
            )

        return super().dispatch(request, *args, **kwargs)


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        context.update(**kwargs)
        return context
