from UserProfile.models import Criminal, CriminalImage, ImageEncoding
from django.shortcuts import render, redirect 

import face_recognition, pickle

def search_image(request):
	matched_criminals = []
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
				matched_criminals.append((ob.criminal,ob.criminal.images.all()[0]))
		if matched_criminals:
			return render(request,'case/imgsearch_results.html',{
				'matches': matched_criminals,
			})
		else:
			return render(request,'case/search_image.html',{'error':'Image Not found in Database.'})
		return redirect('case-index')
	return render(request,'case/search_image.html')