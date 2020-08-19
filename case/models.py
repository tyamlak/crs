from django.db import models
from UserProfile.models import Police, Criminal, Plaintiff, Witness
from datetime import datetime


class Case(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    police_set = models.ManyToManyField(Police)
    criminals = models.ManyToManyField(Criminal)
    plaintiffs = models.ManyToManyField(Plaintiff)
    witness_set = models.ManyToManyField(Witness)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=False)


class CaseFile(models.Model):

    def upload_location(self,file_name):
        return f'case-id-{self.case.pk}/{file_name}'
        
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300,blank=True)
    case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='case_files',blank=False)
    file = models.FileField(upload_to=upload_location,blank=False)

class ActivityLog(models.Model):

    logged_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=False)

    def __str__(self):
        return 'Took place on ' + datetime.strftime(self.logged_at,'%X %d/%m/%Y')