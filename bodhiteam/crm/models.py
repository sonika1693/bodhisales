from django.db import models
from membership.models import *


# Create your models here.
class InstituteStatus(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class UpdateRequirementsStatus(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class UpdatesRequirements(models.Model):
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(to=UpdateRequirementsStatus, on_delete=models.PROTECT, related_name='status')

    def __str__(self) -> str:
        return self.description


class Institute(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    date_of_conversion = models.DateField(null=True, blank=True)
    status = models.ForeignKey(to=InstituteStatus, on_delete=models.PROTECT, related_name='status')
    amount_of_conversion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    update_requirements = models.ManyToManyField(to=UpdatesRequirements, null=True, blank=True, related_name='institute_requirements')
    converted_by = models.ForeignKey(to=SalesExecutive, on_delete=models.SET_NULL, null=True, blank=True, related_name='converted_by')

    def __str__(self) -> str:
        return self.name


