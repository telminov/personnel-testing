# -*- coding:utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'Логин', 'class': 'form-control'}
        self.fields['password'].widget.attrs = {'placeholder': 'Пароль', 'class': 'form-control'}
        self.fields['username'].label = ''
        self.fields['password'].label = ''
