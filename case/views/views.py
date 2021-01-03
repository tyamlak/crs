from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from UserProfile.models import Person, ImageEncoding, Criminal, CriminalImage
from random import randint

from case.utils import log_activity
from UserProfile.forms import CriminalImageForm

from case.models import Location
from django.http.response import JsonResponse


def get_map(request):
	if request.POST:
		lat = request.POST.get('latitude')
		lng = request.POST.get('longtude')
		c_location = Location(lat=float(lat),lng=float(lng))
		c_location.save()
		print("(lat,lng): ",lat,', ',lng)
		data = {
			'location': 'Received Location of Crimes in Addis',
		}
		return JsonResponse(data)
	return render(request,'case/maps_location.html')

def map_dist(request):
	if request.POST:
		c_locations = Location.objects.all()
		locations = []
		case_id = []
		for lc in c_locations:
			locations.append((lc.lat,lc.lng))
			case_id.append(randint(1,123))
		data = {
			'locations':locations,
			'case_id':case_id,
		}
		return JsonResponse(data)
	return render(request,'case/map_dist.html')

@log_activity
def index(request,message=None):
	return render(
		request,'case/index.html',{
			'login_required':False
		}
	)

def criminal_detail(request,pk):
	ob = Criminal.objects.get(pk=pk)
	images = ob.images.all()
	image_url = '' # url(static) of Null image
	if len(images) >= 0:
		image_url = images[0].image.url 
	return render(
		request,'case/criminal_detail.html',{
			'person':ob.profile,'image_url':image_url
		}
	)


def add_image(request):
	if request.POST:
		image_form = CriminalImageForm(request.POST,request.FILES)
		if image_form.is_valid():
			pk = image_form.instance.criminal_id
			criminal = Criminal.objects.get(pk=pk)
			uploaded_image = request.FILES.get('image')
			image_model = CriminalImage(image=uploaded_image,criminal=criminal)
			image_model.save()
			print(f'Redirecting to {pk}')
			return redirect('criminal',pk)

	image_form = CriminalImageForm()
	return render(
		request,'case/add_image.html',{
			'image_form':image_form,
		}
	)