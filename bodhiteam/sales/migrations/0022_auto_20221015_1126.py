# Generated by Django 3.1.7 on 2022-10-15 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0021_auto_20221012_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversion',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 66462)),
        ),
        migrations.AlterField(
            model_name='demofeedback',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 63208)),
        ),
        migrations.AlterField(
            model_name='demofeedback_and_leadfeedback_notifications',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 65701)),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 61908)),
        ),
        migrations.AlterField(
            model_name='lead',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 59388)),
        ),
        migrations.AlterField(
            model_name='massages',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 64102)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 64833)),
        ),
        migrations.AlterField(
            model_name='successfullylead',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 11, 26, 50, 61184)),
        ),
    ]