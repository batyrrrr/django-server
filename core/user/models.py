from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a User with an email, username and password."""
        if not username:
            raise TypeError("User must have a username.")
        elif not email:
            raise TypeError("User must have an email.")
        elif not password:
            raise TypeError("User must have a password.")

        # Normalizing email by lowercase
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        """Create and return a `User` with superuser (admin) permissions."""
        if not username:
            raise TypeError("Superuser must have a username.")
        elif not email:
            raise TypeError("Superuser must have an email.")
        elif not password:
            raise TypeError("Superuser must have a password.")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    # This will be required when creating an account
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def fullname(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    @property
    def user_repositories(self):
        """Return all repositories created by the user."""
        return self.user_repository.all()

    @property
    def is_staff(self):
        """Return True if the user is a staff member."""
        return self.is_superuser
