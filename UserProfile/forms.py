from django.forms import ModelForm
from .models import Person, Criminal, CriminalImage, PhoneNumber, Residence, Work

class PersonForm(ModelForm):
    class Meta:
        model = Person
        # fields = ['first_name','middle_name','last_name']
        exclude = ['phone_number','living_address','work']

class PhoneForm(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['mobile']
    
class ResidenceForm(ModelForm):
    class Meta:
        model = Residence
        exclude= []
    
class WorkForm(ModelForm):
    class Meta:
        model = Work
        exclude = []

class CriminalForm(ModelForm):
    class Meta:
        model = Criminal
        exclude = []

class CriminalImageForm(ModelForm):
    class Meta:
        model = CriminalImage
        exclude = ['image']