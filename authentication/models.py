import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


''' Member Abstract User Manager'''
class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('You must provide an email address.'))
        if not phone_number:
            raise ValueError(_('You must provide a phone number.'))
        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, email=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        
        user = self.create_user(
            phone_number=phone_number,
            email=email,  
            **extra_fields
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

def upload_profile_image(instance, filename):
    return f'{uuid.uuid4()}/{filename}'

''' Member Abstract User '''
class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=254)
    phone_number = PhoneNumberField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to=upload_profile_image, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    accept_terms = models.BooleanField(default=False)
    chama = models.ForeignKey('account.Chama', on_delete=models.CASCADE, null=True,blank=True)

    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = 'Member'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        get_latest_by = ['-date_joined']

    def get_username(self) -> str:
        return f'{self.phone_number}'