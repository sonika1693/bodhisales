from email.policy import default
from random import choices
from tabnanny import verbose
from django.db import models
from membership.models import *
# Create your models here.

class ProjectStatus(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserStatus(models.Model):
    title = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# class TaskStatus(models.Model):
#     title = models.CharField(max_length=50,null=True,blank=True)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.title

def default_status():
    ds = ProjectStatus.objects.get(title='Created')
    return ds

class Task(models.Model):
    assignedTo = models.ForeignKey(TechPerson, related_name='assigned_head', on_delete=models.CASCADE)
    workedBy = models.ManyToManyField(TechPerson,related_name='assigned_developers',null=True,blank=True)
    institute = models.CharField(max_length=50,null=True,blank=True)#make foregin key
    task_title = models.CharField(max_length=100,blank=True,null=True)
    task_description = models.TextField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    due_date = models.DateTimeField(blank=True,null=True)
    additional_details = models.TextField(blank=True,null=True)
    project_status = \
    models.ForeignKey(ProjectStatus, default=default_status, on_delete=models.PROTECT,related_name="project_status",null=True,blank=True)

    def __str__(self):
        return self.task_title

def default_user_status():
    user_status = UserStatus.objects.get(title='Unseen')
    return user_status

class DeveloperReport(models.Model):
    developer = models.ForeignKey(TechPerson, on_delete=models.CASCADE,related_name="project_devloper")
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="developer_task")
    developer_issues = models.TextField(blank=True,null=True)
    status = models.ForeignKey(UserStatus, default=default_user_status, related_name="users_status", null=True, blank=True, on_delete=models.PROTECT)
    task_status = models.ForeignKey(ProjectStatus,default=default_status, related_name="tasks_status", null=True, blank=True, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task.task_title

    class Meta:
        verbose_name = "Developer Task"
        verbose_name_plural = "Developers Tasks"
