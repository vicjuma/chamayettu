import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# from account.models import Chama
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, firstname, lastname, middlename, password=None, **extra_fields):

        user = self.model(
            phone_number=phone_number,
            firstname=firstname,
            lastname=lastname,
            middlename=middlename,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, firstname=None, lastname=None, middlename=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        
        user = self.create_user(
            phone_number=phone_number,
            firstname=firstname,
            lastname=lastname,
            middlename=middlename,
            **extra_fields
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

def upload_profile_image(instance, filename):
    return f'{uuid.uuid4()}/{filename}'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=254)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to=upload_profile_image, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # chama = models.ForeignKey(Chama, on_delete=models.CASCADE, null=True)

    username = None
    email = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'

    def get_short_name(self):
        return self.firstname

    def get_username(self) -> str:
        return f'{self.phone_number}'