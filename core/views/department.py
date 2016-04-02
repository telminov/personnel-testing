# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models import UserExamination, Department, User
from core.views.base import ListView


class DepartmentsListView(ListView):
    model = Department
    template_name = 'core/departments.html'
    context_object_name = 'departments'
    title = 'Выбор отдела для детальной статистики'

    def get_queryset(self):
        return self.request.user.departments_owner.all()
departments_list_view = DepartmentsListView.as_view()


class DepartmentUsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'core/department_users.html'
    _department = None

    def get_department(self):
        if not self._department:
            self._department = self.request.user.departments_owner.get(id=self.kwargs['department_id'])
        return self._department

    def get_title(self):
        return 'Выбор пользователя отдела «%s» для детальной статистики' % self.get_department()

    def get_context_data(self, **kwargs):
        context = super(DepartmentUsersListView, self).get_context_data(**kwargs)
        context['department'] = self.get_department()
        return context

    def get_queryset(self):
        return self.model.objects.filter(departments__in=[self.kwargs['department_id']])
department_users_list_view = DepartmentUsersListView.as_view()


class DepartmentUserExaminationsListView(ListView):
    model = UserExamination
    context_object_name = 'user_examinations'
    template_name = 'core/department_user_examinations.html'
    _user = None
    _department = None

    def get_department(self):
        if not self._department:
            self._department = self.request.user.departments_owner.get(id=self.kwargs['department_id'])
        return self._department

    def get_user(self):
        if not self._user:
            department = self.get_department()
            self._user = department.employees.get(id=self.kwargs['user_id'])
        return self._user

    def get_queryset(self):
        return self.model.objects.filter(user=self.get_user())

    def get_context_data(self, **kwargs):
        context = super(DepartmentUserExaminationsListView, self).get_context_data(**kwargs)
        context['department'] = self.get_department()
        context['user'] = self.get_user()
        return context

    def get_title(self):
        return 'Отдел %s, пользователь %s' % (self.get_department(), self.get_user())
department_user_examinations_list_view = DepartmentUserExaminationsListView.as_view()
