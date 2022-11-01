from django.contrib import admin
from membership.models import *
# Register your models here.

class SalesExecutiveAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ('joiningDate','typeExecutive')
    list_display = ("name","typeExecutive","joiningDate","executiveUser","salesNumber")

class TechExecutiveAdmin(admin.ModelAdmin):
    list_display = ("name","typeTech","joiningDate")

admin.site.register(SalesExecutive,SalesExecutiveAdmin)
admin.site.register(TechPerson,TechExecutiveAdmin)
admin.site.register(Technology)



