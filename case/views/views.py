from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from UserProfile.models import Person, ImageEncoding, Criminal, CriminalImage
from random import randint

from case.utils import log_activity
from UserProfile.forms import CriminalImageForm


def get_map(request):
	return render(request,'case/ac_map.html')

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