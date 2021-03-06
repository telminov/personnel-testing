# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect

from core.forms import UserCreateForm, UserSearchForm, UserUpdateForm
from core.models import User
from core.views.base import CreateOrUpdateView, ListView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse


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


class UserDeletedListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'core/management/deleted_users.html'
    title = 'Управление удалёнными пользователями'

    def get_queryset(self):
        return self.model.default_objects.filter(deleted_at__isnull=False)

    def post(self):
        pass
user_deleted_list_view = UserDeletedListView.as_view()


class UserCreateOrUpdateView(CreateOrUpdateView):
    model = User
    form_class_create = UserCreateForm
    form_class_update = UserUpdateForm
    template_name = 'core/management/user_edit.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user_list_view')

    def get_initial(self):
        initial = {}
        if self.is_update():
            initial['departments'] = self.get_object().departments.all()
            initial['user_id'] = self.object.id
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


class UserDeleteView(DeleteView):
    model = User
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user_list_view')
    template_name = 'core/management/user_delete.html'
    title = 'Удаление пользователя'
user_delete_view = UserDeleteView.as_view()


def user_undelete_view(request, user_id):
    user = User.default_objects.get(id=user_id)
    user.deleted_at = None
    user.save()
    return redirect(reverse('user_list_view'))
