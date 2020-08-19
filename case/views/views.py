from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from UserProfile.forms import *
from UserProfile.models import Person, PhoneNumber, Work, Residence, ImageEncoding, Criminal
from random import randint

from case.utils import log_activity


def get_map(request):
	return render(request,'case/ac_map.html')

@log_activity
def index(request):
	return render(
		request,'case/index.html',{
			'login_required':False
		}
	)

def criminal_detail(request,pk):
	ob = Criminal.objects.get(pk=pk)
	img = ob.images.all()[randint(0,len(ob.images.all())-1)]
	return render(
		request,'case/criminal_detail.html',{
			'person':ob,'img':img
		}
	)


def add_image(request):
	if request.POST:
		image_form = CriminalImageForm(request.POST,request.FILES)
		if image_form.is_valid():
			pk = image_form.instance.criminal_id
			image_form.instance.save()
			print(f'Redirecting to {pk}')
			return redirect('criminal',pk)

	image_form = CriminalImageForm()
	return render(
		request,'case/add_image.html',{
			'image_form':image_form,
		}
	)

def search_image(request):
	if request.POST:
		file = request.FILES.get('image_file')
		import face_recognition, pickle
		new_image = face_recognition.load_image_file(file)
		if new_image is None:
			print('Image could not be opened')
			return redirect('case-index')
		new_encodings = face_recognition.face_encodings(new_image)
		ie_models = ImageEncoding.objects.all()
		for ob in ie_models:
			encoding = pickle.loads(ob.encoding)
			match = face_recognition.compare_faces(new_encodings,encoding)
			if True in match:
				return redirect('criminal',ob.criminal_id)
			else:
				return render('case/index.html',{'error':'Image Not found in Database.'})
		return redirect('case-index')
	return render(request,'case/search_image.html')



def is_form_valid(f):
	if f.is_valid():
		return True
	return False


#@login_required # requires(police/data_encoder)decorators
def create_case(request):
	if request.POST:
		error = 'Model Not Saved.'
		phone_form = PhoneForm(request.POST,request.FILES)
		person_form = PersonForm(request.POST,request.FILES)
		residence_form = ResidenceForm(request.POST,request.FILES)
		work_form = WorkForm(request.POST,request.FILES)
		if person_form.is_valid():
			person = person_form.instance
			forms = [phone_form,residence_form,work_form]
			result = map(is_form_valid,forms)
			if all(result):
				work_form.instance.save()
				residence_form.instance.save()
				phone_form.instance.save()
				person.work = work_form.instance
				person.phone_number = phone_form.instance
				person.living_address = residence_form.instance
				person.save()
				error = 'Data saved Successfully.'
		return render(
			request,'case/index.html',{
				'error':error
			}
		)
	person = PersonForm()
	image_form = CriminalImageForm()
	phone = PhoneForm()
	work = WorkForm()
	residence = ResidenceForm()
	
	return render(
		request,'case/create_case.html',{
			'person':person,
			'image_form':image_form,
			'phone':phone,
			'work':work,
			'residence':residence,
		}
	)