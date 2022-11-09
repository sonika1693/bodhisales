# Generated by Django 3.1.7 on 2022-11-04 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0026_auto_20221104_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversion',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 191877)),
        ),
        migrations.AlterField(
            model_name='demofeedback',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 188850)),
        ),
        migrations.AlterField(
            model_name='demofeedback_and_leadfeedback_notifications',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 191272)),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 187648)),
        ),
        migrations.AlterField(
            model_name='lead',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 185526)),
        ),
        migrations.AlterField(
            model_name='massages',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 189836)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 190541)),
        ),
        migrations.AlterField(
            model_name='successfullylead',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 4, 16, 2, 51, 187080)),
        ),
    ]