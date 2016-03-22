
from django.contrib.auth import get_user_model


class BaseAuthBackend(object):
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class EmailAuthBackend(BaseAuthBackend):
    def authenticate(self, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None


class UsernameAuthBackend(BaseAuthBackend):
    def authenticate(self, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
