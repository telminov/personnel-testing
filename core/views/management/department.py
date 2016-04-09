# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from core.forms import DepartmentEditForm
from core.models import Department, UserExamination
from core.views.base import CreateOrUpdateView, ListView, DetailView
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
    template_name = 'core/base/base_edit.html'
    pk_url_kwarg = 'department_id'
    success_url = reverse_lazy('department_list_view')

    def get_title(self):
        if self.is_create():
            return 'Создание отдела'
        else:
            return 'Редактирование отдела %s' % self.get_object()
department_create_or_update_view = DepartmentCreateOrUpdateView.as_view()