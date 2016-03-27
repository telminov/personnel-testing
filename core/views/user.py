# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import UserCreateForm, UserSearchForm, UserUpdateForm
from core.models import User
from core.views.base import CreateOrUpdateView, ListView
from django.core.urlresolvers import reverse_lazy


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'core/management/users.html'
    title = 'Управление пользователями'

    def get_queryset(self):
        qs = super(UserListView, self).get_queryset()
        if self.request.GET.get('department'):
            qs = qs.filter(departments__in=[self.request.GET['department']])
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['form'] = UserSearchForm(self.request.GET or None)
        return context
user_list_view = UserListView.as_view()


class UserCreateOrUpdateView(CreateOrUpdateView):
    model = User
    form_class_create = UserCreateForm
    form_class_update = UserUpdateForm
    template_name = 'core/base/base_edit.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user_list_view')

    def get_initial(self):
        initial = {}
        if self.is_update():
            initial['departments'] = self.get_object().departments.all()
        return initial

    def form_valid(self, form, commit=True):
        redirect = super(UserCreateOrUpdateView, self).form_valid(form, commit=False)
        if self.is_create():
            self.object.set_password(form.cleaned_data['password'])
            self.object.save()
        self.object.save()
        self.object.departments.clear()
        for department in form.cleaned_data.get('departments', []):
            self.object.departments.add(department)
        return redirect

    def get_title(self):
        if self.is_create():
            return 'Создание пользователя'
        else:
            user = self.get_object()
            return 'Редактирование пользователя %s (%s)' % (user.username, user.email or 'email отсутствует')

user_create_or_update_view = UserCreateOrUpdateView.as_view()
