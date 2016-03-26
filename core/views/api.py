# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models import User, Department
from core.forms import ApiUserImportForm, ApiDepartmentImportForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def department_import(request):
    if not request.POST:
        return JsonResponse({'errors': 'Empty POST'}, status=422)

    form = ApiDepartmentImportForm(request.POST)
    if form.is_valid():
        department = form.save()
        return JsonResponse({'name': department.name, 'id': department.id})
    else:
        return JsonResponse({'errors': form.errors}, status=422)


@csrf_exempt
def user_import(request):
    if not request.POST:
        return JsonResponse({'errors': 'Empty POST'}, status=422)

    form = ApiUserImportForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        raw_password = user.set_random_password(commit=True)
        user.departments.add(form.cleaned_data['department'])
        return JsonResponse({'username': user.username, 'email': user.email, 'password': raw_password})
    else:
        return JsonResponse({'errors': form.errors}, status=422)
