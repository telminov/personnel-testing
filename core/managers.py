# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class UserDefaultManager(UserManager):
    pass


class UserExcludeDeletedManager(UserManager):
    def get_queryset(self):
        return super(UserExcludeDeletedManager, self).get_queryset().filter(deleted_at__isnull=True)


class DefaultManager(models.Manager):
    pass


class ExcludeDeletedManager(models.Manager):
    def get_queryset(self):
        return super(ExcludeDeletedManager, self).get_queryset().filter(deleted_at__isnull=True)
