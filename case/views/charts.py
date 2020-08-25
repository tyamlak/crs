from django.shortcuts import render
from django.views.generic import View
from case.models import Case
from UserProfile.models import Person

from rest_framework.response import Response 
from rest_framework.views import APIView
from datetime import datetime

class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'case/charts.html')

class CrimeTypeDist(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        severe = Case.objects.filter(category='Severe').count()
        medium = Case.objects.filter(category='Medium').count()
        light = Case.objects.filter(category='Light').count()
        data = {
            'chart_type': 'bar',
            'stat': [severe,medium,light],
            'labels':["Severe","Medium","Light"],
            'label': 'Number of Crimes via type'
        }
        return Response(data)

class SexDist(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        no_of_male = Person.objects.filter(sex='M').count()
        no_of_female = Person.objects.all().count() - no_of_male
        data = {
            'chart_type':'doughnut',
            'stat':[no_of_male,no_of_female],
            'labels':['Male','Female'],
        }
        return Response(data)

class MonthlyCrimeDist(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self,request,year=None,format=None):
        label = "Monthly Cases"
        if not year:
            year = datetime.utcnow().year
            label = 'Monthly cases for %d'%year
        else:
            label = 'Monthly cases for %d'%year
        labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        monthly_crimes = []
        all_cases = Case.objects.filter(date_created__year=year)
        for i in range(1,13):
            crime_count = all_cases.filter(date_created__month=i).count()
            monthly_crimes.append(crime_count)
        data = {
            'chart_type':'bar',
            'stat':monthly_crimes,
            'labels':labels,
            'label':label
        }
        return Response(data)


class YearlyCrimeDist(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        labels = []
        yearly_cases = []
        for i in range(20):
            year = 2000 + i
            case_count = Case.objects.filter(date_created__year=year).count()
            labels.append(str(year))
            yearly_cases.append(case_count)
        data = {
            'chart_type':'bar',
            'stat':yearly_cases,
            'labels':labels,
            'label':'No of Cases from 2000-2020'
        }
        return Response(data)



__all__ = ['HomeView','CrimeTypeDist','SexDist','MonthlyCrimeDist','YearlyCrimeDist']