<<<<<<< HEAD
from .models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailOrPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = User.objects.get(Q(email=username) | Q(phone=username))
            print(f"User found: {user}")

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

=======
from .models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailOrPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = User.objects.get(Q(email=username) | Q(phone=username))
            print(f"User found: {user}")

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

>>>>>>> 7159795b6044deffa8701f4b9b7a29f57ca8987b
        return None