from django.test import TestCase

from UserProfile.models import Person, Criminal, CriminalImage
from .utils import save_image_encodings
from .init_db import gen_person


class FaceRecognitionTest(TestCase):

    def test_image_with_face_is_flagged_true(self):
        from django.core.files.base import File

        p = gen_person()
        c = Criminal(profile=p)
        c.save()

        f = open('case/test_data/face.jpg','rb')
        image_file = File(f)
        c_image = CriminalImage(criminal=c,image=image_file)
        c_image.save()

        save_image_encodings(c_image.pk)
        assert c_image.has_face == True, "Error in flagging image with face."
