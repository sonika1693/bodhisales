# Generated by Django 3.1.6 on 2021-04-15 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskAssignToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(blank=True, max_length=500, null=True)),
                ('task', models.TextField()),
                ('taskStart_date', models.DateTimeField(blank=True, null=True)),
                ('taskEnd_date', models.DateTimeField(blank=True, null=True)),
                ('teck_user_issues', models.TextField(blank=True, null=True)),
                ('is_task_ongoing', models.BooleanField(default=False)),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_assign', to='membership.techperson')),
                ('workedBy', models.ManyToManyField(blank=True, null=True, related_name='users_assign', to='membership.TechPerson')),
            ],
        ),
    ]
