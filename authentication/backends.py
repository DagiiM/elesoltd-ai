from django.contrib.auth.backends import BaseBackend
from authentication.models import User
from django.db.models import Q


class CustomAuth(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the user exists with the given username or email or phone_number
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(phone_number=username))
        except User.DoesNotExist:
            return None

        # Check the password
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
