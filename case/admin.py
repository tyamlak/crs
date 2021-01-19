from django.contrib import admin
from case.models import CaseCategory
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register((CaseCategory,))
admin.site.unregister((Group,))
admin.site.site_header = 'Criminal Recording System Adminstration'