from django.urls import path
from .views import (index, create_case, add_image, search_image, 
    criminal_detail, get_map, edit_criminal_info, edit_case, 
    add_criminal_to_case, add_plaintiff_to_case, add_witness_to_case
    )
from .views.charts import (
    HomeView, CrimeTypeDist, SexDist, YearlyCrimeDist, MonthlyCrimeDist
)

urlpatterns = [
    path('',index,name='case-index'),
    path('new',create_case,name='new-case'),
    path('edit/<int:pk>',edit_case,name='edit-case'),
    path('add-image',add_image,name='add_image'),
    path('imgsearch',search_image,name='search-image'),
    path('criminal/<int:pk>/',criminal_detail,name='criminal'),
    path('stats',HomeView.as_view(),name='charts'),
    path('api/crimes',CrimeTypeDist.as_view()),
    path('api/sex_dist',SexDist.as_view()),
    path('api/monthly/<int:year>/',MonthlyCrimeDist.as_view()),
    path('api/monthly',MonthlyCrimeDist.as_view()),
    path('api/yearly',YearlyCrimeDist.as_view()),
    path('edit/criminal/<int:pk>',edit_criminal_info,name='edit-c-in-case'),
    path('<int:pk>',edit_case,name='manage-case'),
    path('<int:pk>/add-criminal',add_criminal_to_case,name='criminal_to_case'),
    path('<int:pk>/add-plaintiff',add_plaintiff_to_case,name='plaintiff_to_case'),
    path('<int:pk>/add-witness',add_witness_to_case,name='witness_to_case'),
    path('maps',get_map,name='maps'),
]