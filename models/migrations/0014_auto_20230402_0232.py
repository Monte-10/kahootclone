# Generated by Django 3.2.1 on 2023-04-02 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0013_auto_20230402_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publicId',
            field=models.IntegerField(default=690936, unique=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='participant_id',
            field=models.IntegerField(default=490880, primary_key=True, serialize=False, unique=True),
        ),
    ]
