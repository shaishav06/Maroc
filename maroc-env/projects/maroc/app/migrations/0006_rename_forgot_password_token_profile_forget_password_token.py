# Generated by Django 4.1.5 on 2023-01-28 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='forgot_password_token',
            new_name='forget_password_token',
        ),
    ]
