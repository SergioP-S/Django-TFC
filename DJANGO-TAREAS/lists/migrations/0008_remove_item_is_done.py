# Generated by Django 5.1.3 on 2024-12-16 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_remove_item_last_modified_remove_item_modified_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='is_done',
        ),
    ]