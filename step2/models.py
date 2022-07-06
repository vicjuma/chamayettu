from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PersonalInfoStepTwo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)

    EMPLOYEMENT = (
        ('SELF_EMPLOYED', 'self employed'),
        ('UNEMPLOYED', 'unemployed'),
        ('PERMANENT', 'permanent'),
        ('PRIVATE_PRACTICE', 'private practice'),
        ('PART_TIME', 'part time'),
        ('CONTRACT', 'contract'),
        ('OTHER', 'other'),
    )

    employment = models.CharField(max_length=50, choices=EMPLOYEMENT)

    INCOME = (
        ('LESS_THAN_5000', 'less than 5000'),
        ('5001_10000', '5001-10,000'),
        ('10001_15000', '10001-15000'),
        ('150001_25000', '150001-25000'),
        ('25001_40000', '25001-40000'),
        ('40001_70000', '40001-70000'),
        ('70001_150000', '70001-150000'),
        ('ABOVE_150000', 'above 150000'),
    )
    income = models.CharField(max_length=50, choices=INCOME)

    def __str__(self) -> str:
        return f'{self.email}'

    class Meta:
        db_table = 'step_two'
        verbose_name = 'Personal Info Step Two'
        verbose_name_plural = 'Personal Info Step Two'
