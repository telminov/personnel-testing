# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from core.forms import DepartmentEditForm
from core.models import Department, UserExamination
from core.views.base import CreateOrUpdateView, ListView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy


class DepartmentListView(ListView):
    model = Department
    context_object_name = 'departments'
    template_name = 'core/management/departments.html'
    title = 'Управление отделами'
department_list_view = DepartmentListView.as_view()


class DepartmentCreateOrUpdateView(CreateOrUpdateView):
    model = Department
    form_class_create = DepartmentEditForm
    form_class_update = DepartmentEditForm
    template_name = 'core/management/department_edit.html'
    pk_url_kwarg = 'department_id'
    success_url = reverse_lazy('department_list_view')

    def get_title(self):
        if self.is_create():
            return 'Создание отдела'
        else:
            return 'Редактирование отдела %s' % self.get_object()
department_create_or_update_view = DepartmentCreateOrUpdateView.as_view()


class DepartmentDeleteView(DeleteView):
    model = Department
    pk_url_kwarg = 'department_id'
    success_url = reverse_lazy('department_list_view')
    template_name = 'core/management/examination_delete.html'
    title = 'Удаление отдела'
department_delete_view = DepartmentDeleteView.as_view()


class DepartmentDeletedListView(ListView):
    model = Department
    context_object_name = 'departments'
    template_name = 'core/management/departments_deleted.html'
    title = 'Управление удалёнными отделами'

    def get_queryset(self):
        return self.model.default_objects.filter(deleted_at__isnull=False)

    def post(self):
        pass
department_deleted_list_view = DepartmentDeletedListView.as_view()
