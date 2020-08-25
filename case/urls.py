from django.urls import path
from .views import index, create_case, add_image, search_image, criminal_detail, get_map
from .views.charts import (
    HomeView, CrimeTypeDist, SexDist, YearlyCrimeDist, MonthlyCrimeDist
)

urlpatterns = [
    path('',index,name='case-index'),
    path('new',create_case,name='new-case'),
    path('add-image',add_image,name='add_image'),
    path('search',search_image,name='search'),
    path('criminal/<int:pk>/',criminal_detail,name='criminal'),
    path('stats',HomeView.as_view(),name='charts'),
    path('api/crimes',CrimeTypeDist.as_view()),
    path('api/sex_dist',SexDist.as_view()),
    path('api/monthly/<int:year>/',MonthlyCrimeDist.as_view()),
    path('api/monthly',MonthlyCrimeDist.as_view()),
    path('api/yearly',YearlyCrimeDist.as_view()),
    path('maps',get_map,name='maps'),
]