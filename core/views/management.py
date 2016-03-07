# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import UserManagementCreateForm, UserManagementSearchForm, UserManagementUpdateForm
from core.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


class UserManagementListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'core/management/users.html'

    def get_queryset(self):
        qs = super(UserManagementListView, self).get_queryset()
        if self.request.GET.get('department'):
            qs = qs.filter(departments__in=[self.request.GET['department']])
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserManagementListView, self).get_context_data(**kwargs)
        context['form'] = UserManagementSearchForm(self.request.GET or None)
        return context
user_management_list_view = UserManagementListView.as_view()


class UserManagementCreateView(CreateView):
    model = User
    form_class = UserManagementCreateForm
    template_name = 'core/management/user_create.html'
    success_url = reverse_lazy('user_management_list_view')

    def form_valid(self, form):
        redirect = super(UserManagementCreateView, self).form_valid(form)
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        for department in form.cleaned_data['departments']:
            form.instance.departments.add(department)
        return redirect
user_management_create_view = UserManagementCreateView.as_view()


class UserManagementUpdateView(UpdateView):
    model = User
    form_class = UserManagementUpdateForm
    template_name = 'core/management/user_create.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user_management_list_view')

    def get_initial(self):
        return {
            'departments': User.objects.get(id=self.kwargs['user_id']).departments.all()
        }

    def form_valid(self, form):
        redirect = super(UserManagementUpdateView, self).form_valid(form)
        form.instance.departments.clear()
        for department in form.cleaned_data['departments']:
            form.instance.departments.add(department)
        return redirect
user_management_update_view = UserManagementUpdateView.as_view()
