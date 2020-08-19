from django.urls import path
from .views import index, create_case, add_image, search_image, criminal_detail, get_map
from .views import get_data,HomeView

urlpatterns = [
    path('',index,name='case-index'),
    path('new',create_case,name='new-case'),
    path('add-image',add_image,name='add_image'),
    path('search',search_image,name='search'),
    path('criminal/<int:pk>/',criminal_detail,name='criminal'),
    path('chart',HomeView.as_view(),name='charts'),
    path('api/data',get_data),
    path('maps',get_map,name='maps'),
]