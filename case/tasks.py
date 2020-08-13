from background_task import background
from UserProfile.models import CriminalImage, ImageEncoding

import pickle
import face_recognition


@background(schedule=60)
def notify_user(user_id):
	# send error message to logged_in user
	print("Notify User id = ",user_id)

@background(schedule=2)
def save_image_encodings(image_id):
	message = ''
	print("Saving image encoding of id ",image_id)
	try:
		ci_model = CriminalImage.objects.get(pk=image_id)
		image = face_recognition.load_image_file(ci_model.image.file)
		face_location = face_recognition.face_locations(image)
		if not len(face_location) or len(face_location)>1:
			message = 'None or Multiple faces'
			raise Exception
		encoding = face_recognition.face_encodings(image,face_location)[0]
		ImageEncoding(encoding=pickle.dumps(encoding),criminal=ci_model.criminal).save()
		print("Image Encoding saved!!!")
	except CriminalImage.DoesNotExist as e:
		message = 'Image instance not found'
	except Exception as e:
		print(e)
	finally:
		print(message)