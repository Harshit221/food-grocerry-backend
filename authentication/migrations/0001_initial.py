# Generated by Django 3.2.9 on 2021-12-05 16:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='admin')),
                ('is_customer', models.BooleanField(default=True, verbose_name='customer')),
                ('is_employee', models.BooleanField(default=False, verbose_name='employee')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('contact_no', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Contact Number', regex='^(\\+[0-9]{1,3})?[0-9]{10}$')])),
                ('email', models.EmailField(max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='authentication.user')),
                ('address', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='authentication.user')),
                ('count', models.IntegerField()),
            ],
        ),
    ]