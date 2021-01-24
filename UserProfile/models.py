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

    def __str__(self):
        return f'{self.mobile}'

class Residence(models.Model):
    house_number = models.PositiveIntegerField()
    kebele = models.PositiveIntegerField()
    subcity = models.CharField(max_length=100)
    former_house_number = models.PositiveIntegerField(default=0)
    former_kebele = models.PositiveIntegerField(default=0)
    former_wereda = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.subcity} Kebele {self.kebele} H.NO {self.house_number}'

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

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

class Criminal(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    is_guilty = models.BooleanField(default=False)
    testimony = models.TextField(blank=True)

    def __str__(self):
        return self.profile.first_name

    @property
    def full_name(self):
        return f'{self.profile.first_name} {self.profile.middle_name} {self.profile.last_name}'

    @property
    def get_pk(self):
        return self.profile.pk

class CriminalImage(models.Model):
    
    def upload_location(self,file_name):
        return f'criminal-id-{self.criminal.get_pk}/images/{file_name}'
    criminal = models.ForeignKey(Criminal,on_delete=models.CASCADE,related_name='images')
    image = models.FileField(upload_to=upload_location) # change to Image field with pillow
    has_face = models.BooleanField(default=False)

class ImageEncoding(models.Model):

    encoding = models.BinaryField(blank=False)
    criminal = models.ForeignKey(Criminal,on_delete=models.CASCADE)

class Plaintiff(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    testimony = models.TextField(blank=False)

class Witness(models.Model):
    profile = models.OneToOneField(Person,primary_key=True,on_delete=models.CASCADE)
    testimony = models.TextField(blank=False)

class Police(models.Model):
    profile = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)

    def __str__(self):
        full_name = self.profile.get_full_name()
        if full_name:
            return full_name
        else:
            return self.profile.username

    @property
    def lastlogin(self):
        return self.profile.last_login

    @property
    def username(self):
        return self.profile.username

class DataEncoder(models.Model):
    profile = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)

    def __str__(self):
        full_name = self.profile.get_full_name()
        if full_name:
            return full_name
        else:
            return self.profile.username

    @property
    def lastlogin(self):
        return self.profile.last_login

    @property
    def username(self):
        return self.profile.username