from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PersonalInfoStepOne(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50)
    idnumber = models.CharField(max_length=50)

    GENDER = (
        ('MALE', 'male'),
        ('FEMALE', 'female'),
    ) 
    gender = models.CharField(max_length=50, choices=GENDER)
    dateofbirth = models.DateField()

    STATUS = (
        ('SINGLE', 'single'),
        ('MARRIED', 'married'),
        ('DIVORCED', 'divorced'),
        ('WIDOWED', 'widowed'),
        ('OTHER', 'other'),
    )
    status = models.CharField(max_length=50, choices=STATUS)

    EDUCATION = (
        ('PRIMARY_SCHOOL', 'primary school'),
        ('HIGH_SCHOOL', 'high school'),
        ('CERTIFICATE', 'certificate'),
        ('DIPLOMA', 'diploma'),
        ('GRADUATE', 'graduate'),
        ('POST_GRADUATE', 'post graduate'),
    )
    education = models.CharField(max_length=50, choices=EDUCATION)

    RESIDENT = (
        ('RESIDENT', 'resident'),
        ('NON_RESIDENT', 'non resident'),
    )
    resident = models.CharField(max_length=50, choices=RESIDENT)
    is_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        db_table = 'step_one'
        verbose_name = 'Personal Info Step One'
        verbose_name_plural = 'Personal Info Step One'
