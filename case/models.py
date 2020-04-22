from django.db import models
from UserProfile.models import Police, Criminal, Plaintiff, Witness


class Case(models.Model):
    police_set = models.ManyToManyField(Police)
    criminals = models.ManyToManyField(Criminal)
    plaintiffs = models.ManyToManyField(Plaintiff)
    witness_set = models.ManyToManyField(Witness)
    category = models.CharField(max_length=100)


class EvidenceFile(models.Model):

    def upload_location(self,file_name):
        return f'case-id-{self.case.pk}/{file_name}'
        
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300,blank=True)
    case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='evidence_files',blank=False)
    file = models.FileField(upload_to=upload_location,blank=False)

