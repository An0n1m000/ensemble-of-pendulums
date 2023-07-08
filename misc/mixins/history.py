from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.template.response import TemplateResponse
from django.views.generic import ListView


class HistoryTableMixin(LoginRequiredMixin, ListView):
    form = None
    object_list = None
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter().order_by('-id')

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        self.object_list = self.get_queryset().filter(user=request.user.uid)
        context = self.get_context_data()
        context[self.context_object_name] = self.object_list

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) -> TemplateResponse:
        history_form = self.form(request.POST)

        if history_form.is_valid():
            form_dict = dict(history_form.cleaned_data)
            form_dict['user'] = request.user.uid
            self.model.objects.create(**form_dict)

        return self.get(request, page=request.POST['page'])
