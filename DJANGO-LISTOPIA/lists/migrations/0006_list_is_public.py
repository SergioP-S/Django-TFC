# Generated by Django 5.1.3 on 2024-12-15 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_remove_item_quantity_remove_item_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
