from django.shortcuts import render, redirect
from UserProfile.models import (
	Criminal, Plaintiff, Witness, Person, Work, PhoneNumber, Residence, CriminalImage,
	Police
)
from UserProfile.forms import PersonForm
from case.form_tools import get_criminal_form_data
from case.models import Case
from case.models import CaseCategory
from case.models import CaseFile
from case.models import Location

from django.contrib.auth import get_user
from django.core.paginator import Paginator


RESULTS_PER_PAGE = 10

#@login_required
def case_list(request):
	cases = Case.objects.all()
	crime_type = None
	crime_type_pk = request.POST.get('crime_type')
	try:
		crime_type = int(crime_type_pk)
	except Exception as e:
		print('Error could not parse int from request')
	if crime_type and crime_type in [c.pk for c in CaseCategory.objects.all()]:
		cases = cases.filter(category=crime_type)
	paginator = Paginator(cases,RESULTS_PER_PAGE)
	page = request.GET.get('page')
	results = paginator.get_page(page)
	return render(
		request,'case/case_list.html',{
			'case_set': results,
		}
	)

#@login_required
def case_detail(request,pk):
	case = Case.objects.get(pk=pk)
	criminals = case.criminals.all()
	plaintiff_set = case.plaintiffs.all()
	witness_set = case.witness_set.all()
	police_set = case.police_set.all()
	return render(request,'case/case_detail.html',{
		'case':case,'criminals':criminals,
		'plaintiff_set': plaintiff_set,
		'witness_set': witness_set,
		'police_set': police_set,
	}
	)

#@login_required # requires(police/data_encoder)decorators
def create_case(request):
	error = ''
	if request.POST:
		created_by_id = 0
		created_by = get_user(request)
		if created_by.is_anonymous:
			error = 'User Not Authenticated'
			return redirect('login')
		else:
			created_by_id = created_by.pk
		case_description = request.POST.get('case_description')
		evidence_files = request.FILES.getlist('evidence')
		assigned_police_list_pk = request.POST.getlist('allowed_polices')
		crime_type_pk = request.POST.get('crime_type')
		crime_type = CaseCategory.objects.get(pk=int(crime_type_pk))
		location_string = request.POST.get('locations')
		for lv in location_string:
			if lv == '':
				locations.remove('')
	
		case = Case()
		case.description = case_description
		case.category = crime_type
		case.save()
		for p_id in assigned_police_list_pk:
			try:
				police = Police.objects.get(pk=int(p_id))
			except Exception as e:
				print('[ERORR]: ',e)
				continue
			case.police_set.add(police)
		for f in evidence_files:
			CaseFile(case=case,file=f).save()
		for ls in locations:
			lat, lng = ls.split(',')
			Location(lat=lat,lng=lng,case=case).save()	
		case.created_by = created_by_id
		case.save()	

		return redirect('edit-case',case.pk)
	case_types = CaseCategory.objects.all()
	list_of_police = Police.objects.all()
	return render(
		request,'case/create_case.html',{
			'case_types':case_types,'police_list':list_of_police,
			'error': error
		}
	)


def edit_case(request,pk):
	if request.POST:
		case = Case.objects.get(pk=pk)

		case_description = request.POST.get('case_description')
		evidence_files = request.FILES.getlist('evidence')
		assigned_police_list_pk = request.POST.getlist('allowed_polices')
		crime_type_pk = request.POST.get('crime_type')
		crime_type = CaseCategory.objects.get(pk=int(crime_type_pk))
		location_string = request.POST.get('locations')
		locations = location_string.split(';')
		for lv in locations:
			if lv == '':
				locations.remove('')

		case.description = case_description
		case.category = crime_type
		case.save()
		for p in case.police_set.all():
			case.police_set.remove(p)
		for p_id in assigned_police_list_pk:
			try:
				police = Police.objects.get(pk=int(p_id))
			except Exception as e:
				print('[ERORR]: ',e)
				continue
			case.police_set.add(police)
		for f in evidence_files:
			CaseFile(case=case,file=f).save()
		for ls in locations:
			lat, lng = ls.split(',')
			Location(lat=lat,lng=lng,case=case).save()
		case.save()
		return redirect('edit-case',pk)

	case = Case.objects.get(pk=pk)
	current_case_type = case.category.crime
	police_set = Police.objects.all()
	allowed_police_set = case.police_set.all()
	all_case_types = CaseCategory.objects.all()
	return render(request,'case/edit_case.html',{
		'case_no':pk,'case':case, 'all_case_types': all_case_types,
		'current_case_type':current_case_type,'police_list':police_set,
		'allowed_police_set':allowed_police_set,
	})
	

def edit_criminal_info(request,pk):
	criminal_ob = Person.objects.get(pk=pk)
	if request.POST:
		form_data = get_criminal_form_data(request)
		print(form_data)
		return redirect('edit-info',pk)
	form = PersonForm(instance=criminal_ob)
	return render(request,'case/edit_info.html',{'form':form})


def add_criminal_to_case(request,pk):
	if request.POST:
		case = Case.objects.get(pk=pk) # raise 404 for EXCEPTIONS
		first_name = request.POST.get('fname')
		middle_name = request.POST.get('mname')
		last_name = request.POST.get('lname')
		sex = request.POST.get('sex')
		age = request.POST.get('age')
		dob = request.POST.get('dob')
		pob = request.POST.get('pob')
		nationality = request.POST.get('nationality')
		ethnicity = request.POST.get('ethnicity')
		religion = request.POST.get('religion')
		income = request.POST.get('income')
		mobile = request.POST.get('mobile')
		house_no = request.POST.get('house_no')
		kebele = request.POST.get('kebele')
		subcity = request.POST.get('subcity')
		former_kebele = request.POST.get('former_kebele')
		former_wereda = request.POST.get('former_wereda')
		salary = request.POST.get('salary')
		work_role = request.POST.get('work_role')
		work_type = request.POST.get('work_type')
		work_address = request.POST.get('work_address')
		photo = request.FILES.get('photo')

		work = Work(
			salary=salary,role=work_role,
			work_type=work_type,address=work_address
		)
		work.save()
		phone = PhoneNumber(
			mobile=mobile
		)
		phone.save()
		residence = Residence(
			house_number=house_no,kebele=kebele,subcity=subcity,
			former_kebele=former_kebele,former_wereda=former_wereda,
		)
		residence.save()
		person = Person(
			first_name=first_name,middle_name=middle_name,last_name=last_name,
			sex=sex,age=age,date_of_birth=dob,place_of_birth=pob,
			nationality=nationality,ethnicity=ethnicity,religion=religion,
			income=income,
			work=work,phone_number=phone,living_address=residence,
		)
		person.save()
		criminal = Criminal(profile=person)
		criminal.save()
		if photo:
			c_image = CriminalImage(criminal=criminal,image=photo)
			c_image.save()
		case.criminals.add(criminal)
		print('Adding criminal to case with pk ',pk)
		return redirect('criminal',criminal.pk)


def add_plaintiff_to_case(request,pk):
	if request.POST:
		case = Case.objects.get(pk=pk) # raise 404 for EXCEPTIONS
		first_name = request.POST.get('fname')
		middle_name = request.POST.get('mname')
		last_name = request.POST.get('lname')
		sex = request.POST.get('sex')
		age = request.POST.get('age')
		dob = request.POST.get('dob')
		pob = request.POST.get('pob')
		nationality = request.POST.get('nationality')
		ethnicity = request.POST.get('ethnicity')
		religion = request.POST.get('religion')
		income = request.POST.get('income')
		mobile = request.POST.get('mobile')
		house_no = request.POST.get('house_no')
		kebele = request.POST.get('kebele')
		subcity = request.POST.get('subcity')
		former_kebele = request.POST.get('former_kebele')
		former_wereda = request.POST.get('former_wereda')
		salary = request.POST.get('salary')
		work_role = request.POST.get('work_role')
		work_type = request.POST.get('work_type')
		work_address = request.POST.get('work_address')

		work = Work(
			salary=salary,role=work_role,
			work_type=work_type,address=work_address
		)
		work.save()
		phone = PhoneNumber(
			mobile=mobile
		)
		phone.save()
		residence = Residence(
			house_number=house_no,kebele=kebele,subcity=subcity,
			former_kebele=former_kebele,former_wereda=former_wereda,
		)
		residence.save()
		person = Person(
			first_name=first_name,middle_name=middle_name,last_name=last_name,
			sex=sex,age=age,date_of_birth=dob,place_of_birth=pob,
			nationality=nationality,ethnicity=ethnicity,religion=religion,
			income=income,
			work=work,phone_number=phone,living_address=residence,
		)
		person.save()
		plaintiff = Plaintiff(profile=person)
		plaintiff.save()
		case.plaintiffs.add(plaintiff)
		print('Adding plaintiff to case with pk ',pk)
		return redirect('manage-case',pk)


def add_witness_to_case(request,pk):
	if request.POST:
		case = Case.objects.get(pk=pk) # raise 404 for EXCEPTIONS
		first_name = request.POST.get('fname')
		middle_name = request.POST.get('mname')
		last_name = request.POST.get('lname')
		sex = request.POST.get('sex')
		age = request.POST.get('age')
		dob = request.POST.get('dob')
		pob = request.POST.get('pob')
		nationality = request.POST.get('nationality')
		ethnicity = request.POST.get('ethnicity')
		religion = request.POST.get('religion')
		income = request.POST.get('income')
		mobile = request.POST.get('mobile')
		house_no = request.POST.get('house_no')
		kebele = request.POST.get('kebele')
		subcity = request.POST.get('subcity')
		former_kebele = request.POST.get('former_kebele')
		former_wereda = request.POST.get('former_wereda')
		salary = request.POST.get('salary')
		work_role = request.POST.get('work_role')
		work_type = request.POST.get('work_type')
		work_address = request.POST.get('work_address')
		testimony = request.POST.get('testimony')

		work = Work(
			salary=salary,role=work_role,
			work_type=work_type,address=work_address
		)
		work.save()
		phone = PhoneNumber(
			mobile=mobile
		)
		phone.save()
		residence = Residence(
			house_number=house_no,kebele=kebele,subcity=subcity,
			former_kebele=former_kebele,former_wereda=former_wereda,
		)
		residence.save()
		person = Person(
			first_name=first_name,middle_name=middle_name,last_name=last_name,
			sex=sex,age=age,date_of_birth=dob,place_of_birth=pob,
			nationality=nationality,ethnicity=ethnicity,religion=religion,
			income=income,
			work=work,phone_number=phone,living_address=residence,
		)
		person.save()
		witness = Witness(profile=person)
		witness.testimony = testimony
		witness.save()
		case.witness_set.add(witness)
		print('Adding witness to case with pk ',pk)
		return redirect('manage-case',pk)