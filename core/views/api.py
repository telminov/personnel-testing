# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models import User
from core.forms import ApiUserImportForm
from django.http import HttpResponse, JsonResponse


def user_import(request):
    if not request.POST:
        return JsonResponse({'errors': 'Empty POST'}, status=422)

    form = ApiUserImportForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        raw_password = user.set_random_password(commit=True)
        return JsonResponse({'username': user.username, 'email': user.email, 'password': raw_password})
    else:
        return JsonResponse({'errors': form.errors}, status=422)
