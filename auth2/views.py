# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import urlparse, urlunparse

from django.template.response import TemplateResponse
from django.utils.http import *
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth.views import auth_login, auth_logout

from django.shortcuts import redirect

from auth2.forms import LoginForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    """
    Почти полная копия стандартного login
    """
    redirect_to = request.GET.get('next', '')

    form = LoginForm(data=request.POST or None, request=request)
    if form.is_valid():

        # Ensure the user-originating redirection url is safe.
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = '/login/'

        # Okay, security check complete. Log the user in.
        auth_login(request, form.get_user())

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        return redirect(redirect_to)

    request.session.set_test_cookie()

    context = {
        'form': form,
        'next': redirect_to,
    }
    return TemplateResponse(request, 'auth2/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('/login/')