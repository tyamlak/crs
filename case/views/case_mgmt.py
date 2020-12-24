from django.shortcuts import render, redirect
from UserProfile.models import (
	Criminal, Plaintiff, Witness, Person, Work, PhoneNumber, Residence, CriminalImage
)
from UserProfile.forms import PersonForm
from case.form_tools import get_criminal_form_data
from case.models import Case


#@login_required # requires(police/data_encoder)decorators
def create_case(request):
	error = ''
	if request.POST:
		error = ''
		return render(
			request,'case/index.html',{
				'error':error
			}
		)
	return render(
		request,'case/create_case.html',{
			'error': error
		}
	)


def edit_case(request,pk):
	if request.POST:
		pass
	return render(request,'case/edit_case.html',{
		'case_no':pk,
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
		case.plaintiff.add(plaintiff)
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