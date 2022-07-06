# Generated by Django 4.0.5 on 2022-07-06 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondGuarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=50, region=None)),
                ('relationship', models.CharField(choices=[('FATHER', 'father'), ('MOTHER', 'mother'), ('BROTHER', 'brother'), ('SISTER', 'sister'), ('SPOUSE', 'spouse'), ('COLLEGUE', 'colleague'), ('FRIEND', 'friend'), ('OTHER', 'other')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Second Guarantor',
                'verbose_name_plural': 'Second Guarantor',
                'db_table': 'second_guarantor',
            },
        ),
        migrations.CreateModel(
            name='FirstGuarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=50, region=None)),
                ('relationship', models.CharField(choices=[('FATHER', 'father'), ('MOTHER', 'mother'), ('BROTHER', 'brother'), ('SISTER', 'sister'), ('SPOUSE', 'spouse'), ('COLLEGUE', 'colleague'), ('FRIEND', 'friend'), ('OTHER', 'other')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'First Guarantor',
                'verbose_name_plural': 'First Guarantor',
                'db_table': 'first_guarantor',
            },
        ),
    ]
