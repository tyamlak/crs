from django.contrib import admin 
from django.urls import path, include
from case.views import index
from UserProfile.views import sign_in, sign_out
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('login',sign_in,name='login'),
    path('logout',sign_out,name='logout'),
    path('case/',include('case.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
