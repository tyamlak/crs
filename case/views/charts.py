from django.shortcuts import render, redirect
from django.views.generic import View
from case.models import Case
from case.models import CaseCategory
from UserProfile.models import Person

from rest_framework.response import Response 
from rest_framework.views import APIView
from datetime import datetime

from rest_framework import permissions
from django.contrib.auth import get_user

class HomeView(View):
    def get(self,request,*args,**kwargs):
        if get_user(request).is_anonymous:
            return redirect('login')
        return render(request,'case/charts.html')

class CrimeTypeDist(APIView):

    authentication_classes = []
    permission_classes = [ permissions.IsAuthenticated, ]

    def get(self,request,format=None):
        cts = CaseCategory.objects.all()
        severe = medium = light = 0
        for ct in cts:
            if ct.crime_type == 'S':
                severe += ct.case_set.all().count()
            elif ct.crime_type == 'M':
                medium += ct.case_set.all().count()
            elif ct.crime_type == 'L':
                light += ct.case_set.all().count()
        data = {
            'chart_type': 'bar',
            'stat': [severe,medium,light],
            'labels':["Severe","Medium","Light"],
            'label': 'Number of Crimes via type'
        }
        return Response(data)


class CrimeDist(APIView):

    authentication_classes = []
    permission_classes = [ permissions.IsAuthenticated, ]

    def get(self,request,format=None):
        cts = CaseCategory.objects.all()
        labels  = []
        stat = []
        chart_type = 'bar'
        year = request.GET.get('year') or None
        if year:
            try:
                year = int(year)
            except Exception as e:
                print("Error parsing int")
        label = 'Number of crimes '
        for ct in cts:
            labels.append(ct.crime)
            if year and year > 0:
                stat.append(ct.case_set.filter(date_created__year=year).count())
            else:
                stat.append(ct.case_set.all().count())
        data = {
            'chart_type':chart_type,
            'stat':stat,
            'labels':labels,
            'label':label,
        }
        return Response(data)


class SexDist(APIView):

    authentication_classes = []
    permission_classes = [ permissions.IsAuthenticated, ]

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
    permission_classes = [ permissions.IsAuthenticated, ]

    def get(self,request,format=None):
        label = "Monthly Cases"
        year = datetime.utcnow().year
        crime_type = None
        try:
            year = int(request.GET.get('year'))
        except Exception as e:
            print('Error while parsing user input',e)
        try:
            crime_type = int(request.GET.get('crime_type')) or None
        except Exception as e:
            print('Error while parsing request for [crime_type]',e)
        label = 'Number of Monthly cases for %d'%year
        labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        monthly_crimes = []
        all_cases = Case.objects.filter(date_created__year=year)
        if (isinstance(crime_type,int))  and (crime_type > 0):
            all_cases = all_cases.filter(category=crime_type)
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
    permission_classes = [ permissions.IsAuthenticated, ]

    def get(self,request,format=None):
        labels = []
        yearly_cases = []
        current_year = datetime.utcnow().year
        crime_type = None
        start_year = int(request.GET.get('from') or (current_year - 4))
        end_year = int(request.GET.get('to') or current_year)
        if start_year > end_year:
            start_year, end_year = end_year, start_year
        try:
            crime_type = int(request.GET.get('crime_type')) or None
        except Exception as e:
            print('Error while parsing request for [crime_type]',e)
        for year in range(start_year,end_year + 1):
            if (not crime_type) or (crime_type <= 0):
                case_count = Case.objects.filter(date_created__year=year).count()
            else:
                case_count = Case.objects.filter(date_created__year=year,category=crime_type).count()
            labels.append(str(year))
            yearly_cases.append(case_count)
        data = {
            'chart_type':'bar',
            'stat':yearly_cases,
            'labels':labels,
            'label':'Number of Yearly Cases from %d - %d'%(start_year,end_year)
        }
        return Response(data)



__all__ = ['HomeView','CrimeTypeDist','SexDist','MonthlyCrimeDist','YearlyCrimeDist','CrimeDist']