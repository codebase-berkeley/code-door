from django.contrib.auth.backends import ModelBackend
from codedoor.models import User, SlackProfile


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, slack_id=None):
        try:
            personal_key = SlackProfile.objects.get(pk=slack_id).prim_key
            return User.objects.get(pk=personal_key)
        except SlackProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None