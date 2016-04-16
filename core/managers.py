# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class UserDefaultManager(UserManager):
    pass


class UserExcludeDeletedManager(UserManager):
    def get_queryset(self):
        return super(UserExcludeDeletedManager, self).get_queryset().filter(deleted_at__isnull=True)
