from django.contrib import admin
from case.models import CaseCategory
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from UserProfile.models import Police

admin.site.register((CaseCategory,))
admin.site.unregister((Group,))
admin.site.site_header = 'Criminal Recording System Adminstration'


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin,self).__init__(*args, **kwargs)
        add_fieldsets = UserAdmin.add_fieldsets
        add_fieldsets[0][1]['fields'] = ('first_name','last_name',) + add_fieldsets[0][1]['fields']
        UserAdmin.add_fieldsets = add_fieldsets

admin.site.unregister((Police,))

@admin.register(Police)
class PoliceAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display += ('username','lastlogin',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'profile':
            query_set = User.objects.filter(is_staff=False,police=None)
            kwargs['queryset'] = query_set
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.unregister((User,))
admin.site.register(User,CustomUserAdmin)