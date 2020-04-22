from django.db import models
from django.contrib.auth.models import User


class Work(models.Model):
    salary = models.PositiveIntegerField()
    role = models.CharField(max_length=100)
    work_type = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class PhoneNumber(models.Model):
    mobile = models.CharField(max_length=25,blank=True)
    house = models.CharField(max_length=25,blank=True)
    work = models.CharField(max_length=25,blank=True)
    neighbor = models.CharField(max_length=25,blank=True)

class Residence(models.Model):
    house_number = models.PositiveIntegerField()
    kebele = models.PositiveIntegerField()
    subcity = models.CharField(max_length=100)
    former_house_number = models.PositiveIntegerField()
    former_kebele = models.PositiveIntegerField()
    former_wereda = models.PositiveIntegerField()

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    age = models.PositiveSmallIntegerField()
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    income = models.PositiveIntegerField()
    phone_number = models.OneToOneField(PhoneNumber,on_delete=models.CASCADE)
    work = models.OneToOneField(Work,on_delete=models.CASCADE)
    living_address = models.OneToOneField(Residence,on_delete=models.CASCADE) 

class Criminal(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    is_guilty = models.BooleanField(default=False)
    testimony = models.TextField(blank=True)

class CriminalImage(models.Model):
    
    def upload_location(self,file_name):
        return f'{file_name}'
    criminal = models.ForeignKey(Criminal,on_delete=models.CASCADE,related_name='images')
    image = models.FileField(upload_to=upload_location) # change to Image field with pillow

class ImageEncoding(models.Model):

    def upload_location(self,file_name):
        return f'{file_name}'
    encoding = models.FileField(upload_to=upload_location)
    criminal = models.ForeignKey(Criminal,on_delete=models.CASCADE)

class Plaintiff(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    testimony = models.TextField(blank=False)

class Witness(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    testimony = models.TextField(blank=False)

class Police(models.Model):
    profile = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)

class DataEncoder(models.Model):
    profile = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
