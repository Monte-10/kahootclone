# Generated by Django 3.2.1 on 2023-04-01 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20230401_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
    ]