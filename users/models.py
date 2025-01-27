from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class Location(models.Model):
    village = models.CharField(max_length=100)
    parish = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Uganda')

    def __str__(self):
        return f"{self.village}, {self.parish}, {self.subcounty}, {self.county}, {self.district}, {self.country}"

    class Meta:
        verbose_name_plural = "Locations"


class AccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, date_of_birth, nin, password=None, location=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        if not username:
            raise ValueError("The Username field is required")
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            nin=nin,
            location=location,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Superuser does not need location
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    nin = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)

    # Role fields
    land_owner = models.BooleanField(default=False)
    surveyor = models.BooleanField(default=False)
    govt_official = models.BooleanField(default=False)
    law_enforcement = models.BooleanField(default=False)

    # Permissions fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth', 'nin']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name_plural = "Accounts"
