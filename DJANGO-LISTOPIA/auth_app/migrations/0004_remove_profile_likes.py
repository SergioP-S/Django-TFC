# Generated by Django 5.1.3 on 2024-11-27 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='likes',
        ),
    ]
