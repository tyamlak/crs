from django.contrib.auth import get_user
from case.models import ActivityLog
from datetime import datetime 

import face_recognition
from UserProfile.models import CriminalImage, ImageEncoding
import pickle


class Base(object):
	def __init__(self,func):
		self.func=func
	def __call__(self,*args,**kwargs):
		self.request = args[0]
		self.logged_in = get_user(self.request)


class log_activity(Base):

	def __call__(self,*args,**kwargs):
		super().__call__(*args)
		act_time = datetime.utcnow()
		func_name = self.func.__name__
		if not self.logged_in.is_anonymous:
			print('[DEBUG] Activity coming from a logged in User.')
			print('type of user ',type(self.logged_in))
		else:
			print('[DEBUG] User not logged in.')
		print('[DEBUG] Function ',func_name,' called at .',datetime.strftime(act_time,'%X %d/%m/%Y'))
		try:
			ActivityLog(logged_at=act_time,description="Activity " + func_name).save()
		except:
			print('[DEBUG] Error while saving object')
		return self.func(*args)


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