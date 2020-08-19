from django.contrib import admin
from UserProfile.models import DataEncoder,Police,Criminal,Person
from case.models import ActivityLog

admin.site.register((DataEncoder,Police,ActivityLog))