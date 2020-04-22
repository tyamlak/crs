from django.contrib import admin
from UserProfile.models import DataEncoder,Police,Criminal,Person

admin.site.register((DataEncoder,Police))