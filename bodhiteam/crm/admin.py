from django.contrib import admin
from .models import *

# Register your models here.


class UpdateRequirementsInline(admin.TabularInline):
    model = Institute.update_requirements.through
    

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']
    list_editable = ['status']
    exclude = ['update_requirements']
    inlines = [UpdateRequirementsInline]


@admin.register(UpdatesRequirements)
class UpdateRequirementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'status']
    list_editable = ['status']


@admin.register(InstituteStatus)
class InstituteStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(UpdateRequirementsStatus)
class UpdateRequirementsStatusAdmin(admin.ModelAdmin):
    pass


