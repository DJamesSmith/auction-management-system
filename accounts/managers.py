<<<<<<< HEAD
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager): # BaseUserManager: Defines How User Is Created

    # These methods tell Django how to create user.
    def create_user(self, email, phone, password=None, **extra_fields):     #extra_fields = {"role": "ADMIN" }
        print(f'User created: {self.model}')
        
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)     # to make the email lowercase"

        user = self.model(email=email, phone=phone, **extra_fields)     # Create a new user instance of the User model.
        user.set_password(password)             # Password hashing
        user.save(using=self._db)
        # user.save()
        return user

    # These methods tell Django how to create Super users.
    def create_superuser(self, email, phone, password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        # Important: Superuser should be ADMIN in our application
        extra_fields.setdefault("role", "ADMIN")

=======
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager): # BaseUserManager: Defines How User Is Created

    # These methods tell Django how to create user.
    def create_user(self, email, phone, password=None, **extra_fields):     #extra_fields = {"role": "ADMIN" }
        print(f'User created: {self.model}')
        
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)     # to make the email lowercase"

        user = self.model(email=email, phone=phone, **extra_fields)     # Create a new user instance of the User model.
        user.set_password(password)             # Password hashing
        user.save(using=self._db)
        # user.save()
        return user

    # These methods tell Django how to create Super users.
    def create_superuser(self, email, phone, password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        # Important: Superuser should be ADMIN in our application
        extra_fields.setdefault("role", "ADMIN")

>>>>>>> 7159795b6044deffa8701f4b9b7a29f57ca8987b
        return self.create_user(email, phone, password, **extra_fields)