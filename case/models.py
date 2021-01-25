from django.db import models
from UserProfile.models import Police, Criminal, Plaintiff, Witness , DataEncoder
from datetime import datetime
from django.contrib.auth.models import User


class CaseCategory(models.Model):

    class Meta:
        verbose_name = "Case Category"

    LIGHT = 'L'
    MEDIUM = 'M'
    SEVERE = 'S'
    CASE_TYPE_CHOICES = (
        (LIGHT,'Light'),
        (MEDIUM,'Medium'),
        (SEVERE,'Severe'),
    )
    crime_type = models.CharField(max_length=100,choices=CASE_TYPE_CHOICES,verbose_name='Case Category')
    crime = models.CharField(max_length=200,blank=False,verbose_name='Crime Type')

    def __str__(self):
        return f'{self.crime} ==> {self.get_crime_type_display()}'

class Case(models.Model):

    class Meta:
        verbose_name = 'Case'

    date_created = models.DateTimeField(auto_now_add=True)
    police_set = models.ManyToManyField(Police)
    criminals = models.ManyToManyField(Criminal)
    plaintiffs = models.ManyToManyField(Plaintiff)
    witness_set = models.ManyToManyField(Witness)
    category = models.ForeignKey(CaseCategory,null=True,on_delete=models.SET_NULL)
    description = models.TextField(blank=False)
    created_by = models.PositiveIntegerField(blank=False,default=0)
    case_closed = models.BooleanField(blank=False,default=False)

    @property
    def get_no_of_criminals(self):
        return self.criminals.all().count

    @property
    def get_no_of_witness(self):
        return self.witness_set.all().count

    @property
    def get_no_of_plaintiffs(self):
        return self.plaintiffs.all().count

    @property
    def get_creator_instance(self):
        user = 'AnonymousUser'
        police = None
        data_encoder = None
        if self.created_by == 0:
            return user
        try: 
            user = User.objects.get(pk=self.created_by)
        except Exception as E:
            print('[Error]: Case Creator with id, ' + str(self.created_by) + 'has been deleted.')
            return user
        if not isinstance(user,str):
            try:
                police = Police.objects.get(profile=user)
                return police
            except Exception as e:
                print('Profile is not police.')
            try:
                data_encoder = DataEncoder.objects.get(profile=user)
                return data_encoder
            except Exception as e:
                print('Profile is not DataEncoder')
        return user 
    
    @property
    def is_closed(self):
        return self.case_closed

class CaseType(models.Model):

    class Meta:
        verbose_name = 'Case Type'

    case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='case_types')

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


class Location(models.Model):

    case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='locations',blank=False)
    lat = models.FloatField(blank=False)
    lng = models.FloatField(blank=False)

    def __str__(self):
        return f'(lat: {self.lat}, lng: {self.lng})'