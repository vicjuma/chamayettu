import uuid
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

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

class ContibutionFrequency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FREQUENCY = (
        ('WEEKLY', 'weekly'),
        ('MONTHLY', 'monthly'),
    )
    frequency = models.CharField(max_length=50, choices=FREQUENCY)

    AMOUNT = (
        ('1000', '1000'),
        ('3000', '3000'),
        ('5000', '5000'),
        ('10000', '10000'),
        ('15000', '15000'),
        ('20000', '20000'),
        ('25000', '25000'),
        ('30000', '30000'),
        ('35000', '35000'),
        ('40000', '40000'),
        ('45000', '45000'),
        ('50000', '50000'),
        ('60000', '60000'),
        ('70000', '70000'),
        ('80000', '80000'),
        ('90000', '90000'),
        ('100000', '100000'),
    )
    amount = models.CharField(max_length=50, choices=AMOUNT)
    is_saved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.frequency}'

    class Meta:
        db_table = 'contribution_frequency'
        verbose_name = 'Contribution Frequency'
        verbose_name_plural = 'Contribution Frequency'


class Chama(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user2')
    user3 = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user3')
    user4 = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user4')
    user5 = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user5')
    user6 = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user6')
    frequency = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def counter(self):
        if self.user is not None:
            return 1
        if self.user2 is not None:
            return 2
        if self.user3 is not None:
           return 3
        if self.user4 is not None:
            return 4
        if self.user5 is not None:
            return 5
        if self.user6 is not None:
            return 6
        return 0

    @property
    def days(self):
        day = 1
        today = datetime.now().day
        created = self.created.day
        if today == created:
            return day
        elif today > created:
            day = today - created
        
        return day

    @property
    def level(self):
        if self.frequency == 'WEEKLY':
            print(self.days)
            if self.days >= 1 and self.days <= 7:
                return 1
            elif self.days >= 8 and self.days <= 14:
                return 2
            elif self.days >= 15 and self.days <= 21:
                return 3

        elif self.frequency == 'MONTHLY':
            if self.days >= 1 and self.days <= 30:
                return 1
            elif self.days >= 31 and self.days <= 60:
                return 2
            elif self.days >= 61 and self.days <= 90:
                return 3

    @property
    def leave(self):
        if self.level == 2:
            return True
        return False

    @property
    def fourth_member(self):
        if self.level == 2:
            return True
        return False

    @property
    def fifth_and_sixth_member(self):
        if self.level == 3:
            return True
        return False

    @property
    def payment_status(self):
        if self.next_payment_date <= datetime.date.today():
            return True
        return False

    @property
    def next_payment_date(self):
        if self.frequency == 'WEEKLY':
            return self.created + timedelta(days=7)
        elif self.frequency == 'MONTHLY':
            return self.created + timedelta(days=30)

    def __str__(self) -> str:
        return f'{self.id}'

    class Meta:
        db_table = 'chama'
        verbose_name = 'Chama'
        verbose_name_plural = 'Chama'