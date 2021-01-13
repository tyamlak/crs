from UserProfile.models import Criminal, CriminalImage, ImageEncoding
from django.shortcuts import render, redirect 

import face_recognition, pickle

from django.core.paginator import Paginator

from hashlib import sha256
import time
from uuid import uuid4

search_results = {}
RESULTS_PER_PAGE = 5

def search_image(request):
	global search_results
	matched_criminals = []
	if ('page' in request.GET) and ('hash' in request.GET):
		page = request.GET.get('page')
		hash_str = request.GET.get('hash')
		matched_criminals = search_results.get(hash_str)
		paginator = Paginator(matched_criminals,RESULTS_PER_PAGE)
		results = paginator.get_page(page)
		return render(request,'case/imgsearch_results.html',{
			'matches':results,'hash':hash_str
		})
	if request.POST:
		file = request.FILES.get('image_file')
		try:
			new_image = face_recognition.load_image_file(file)
		except Exception as e:
			print("Exception Occured while opening uploaded file",e)
			return render(request,'case/search_image.html',{
				'error':'Unable to open Uploaded file as Image.'
			})
		if new_image is None:
			print('Error: Submitted file Couldn\'t be opened as image.')
			return redirect('case-index')
		new_encodings = face_recognition.face_encodings(new_image)
		ie_models = ImageEncoding.objects.all()
		for ob in ie_models:
			encoding = pickle.loads(ob.encoding)
			matches = face_recognition.compare_faces(new_encodings,encoding)
			if True in matches:
				image_url = '' 
				if len(ob.criminal.images.all()) > 0:
					image_url = ob.criminal.images.all()[0].image.url
					print("Image url is ",image_url)
				matched_criminals.append((ob.criminal.profile,image_url))
		if matched_criminals:
			paginator = Paginator(matched_criminals,RESULTS_PER_PAGE)
			page = request.GET.get('page')
			results = paginator.get_page(page)
			hash_value = sha256((str(time.time()) + str(uuid4()).replace('-','') ).encode()).hexdigest()
			search_results.update({hash_value:matched_criminals})
			return render(request,'case/imgsearch_results.html',{
				'matches': results,'hash':hash_value
			})
		else:
			return render(request,'case/search_image.html',{'error':'Image Not found in Database.'})
		return redirect('case-index')
	return render(request,'case/search_image.html')


def search(request):
	return render(request,'case/search.html')