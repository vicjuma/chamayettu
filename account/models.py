from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ContibutionFrequency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FREQUENCY = (
        ('WEEKLY', 'weekly'),
        ('MONTHLY', 'monthly'),
    )
    frequency = models.CharField(max_length=50, choices=FREQUENCY)

    AMOUNT = (
        ('1', '1'),
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
    id = models.AutoField(primary_key=True)
    frequency = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    group_complete = models.BooleanField(default=False)

    @property
    def counter(self):
        return User.objects.filter(chama_id=self.id).count()

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
    def days_left(self):
        if self.frequency == 'WEEKLY':
            return 7 - self.days
        elif self.frequency == 'MONTHLY':
            return 30 - self.days

    # if days_left is 0 change date created to today
    @property
    def start_date(self):
        if self.days_left == 0:
            self.created = datetime.now()
            self.save()
            return self.created
        else:
            return self.created

    @property
    def level(self):
        if self.frequency == 'WEEKLY':
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

class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.user.username}'

    class Meta:
        db_table = 'points'
        verbose_name = 'Points'
        verbose_name_plural = 'Points'