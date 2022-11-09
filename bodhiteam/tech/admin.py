from django.contrib import admin
from .models import *

# Register your models here.
class TaskList(admin.ModelAdmin):
    list_display = ["assignedTo","institute","create_date","project_status"]
    
class DeveloperReportData(admin.ModelAdmin):
    list_display = ["developer","task","status","date"]

admin.site.register(ProjectStatus)
admin.site.register(UserStatus)
admin.site.register(Task,TaskList)   
admin.site.register(DeveloperReport,DeveloperReportData)
