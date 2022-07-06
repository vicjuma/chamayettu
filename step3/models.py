from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class FirstGuarantor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = PhoneNumberField(max_length=50)

    RELASHIONSHIP = (
        ('FATHER', 'father'),
        ('MOTHER', 'mother'),
        ('BROTHER', 'brother'),
        ('SISTER', 'sister'),
        ('SPOUSE', 'spouse'),
        ('COLLEGUE', 'colleague'),
        ('FRIEND', 'friend'),
        ('OTHER', 'other'),
    )
    relationship = models.CharField(max_length=50, choices=RELASHIONSHIP)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        db_table = 'first_guarantor'
        verbose_name = 'First Guarantor'
        verbose_name_plural = 'First Guarantor'


class SecondGuarantor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = PhoneNumberField(max_length=50)

    RELASHIONSHIP = (
        ('FATHER', 'father'),
        ('MOTHER', 'mother'),
        ('BROTHER', 'brother'),
        ('SISTER', 'sister'),
        ('SPOUSE', 'spouse'),
        ('COLLEGUE', 'colleague'),
        ('FRIEND', 'friend'),
        ('OTHER', 'other'),
    )
    relationship = models.CharField(max_length=50, choices=RELASHIONSHIP)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        db_table = 'second_guarantor'
        verbose_name = 'Second Guarantor'
        verbose_name_plural = 'Second Guarantor'