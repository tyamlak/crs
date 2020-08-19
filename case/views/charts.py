from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from case.models import Case

class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'case/charts.html',{'customers':10})


def get_data(request,*args,**kwargs):
    severe = Case.objects.filter(category='Severe').count()
    medium = Case.objects.filter(category='Medium').count()
    light = Case.objects.filter(category='Light').count()
    data = {
        "chart_type": 'bar',
        "crime_stat": [severe,medium,light]
    }
    return JsonResponse(data)