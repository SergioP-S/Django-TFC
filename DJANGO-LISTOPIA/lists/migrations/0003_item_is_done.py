# Generated by Django 5.0.7 on 2024-10-01 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_rename_item_name_item_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
