# Generated by Django 5.1.3 on 2024-11-21 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_last_modified_item_modified_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='weight',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='test', max_length=256),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('color', models.CharField(default='#007bff', max_length=7)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.list')),
            ],
        ),
    ]
