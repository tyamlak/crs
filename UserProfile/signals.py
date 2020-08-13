from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CriminalImage
from case.tasks import save_image_encodings


@receiver(post_save,sender=CriminalImage)
def schedule_image_encoding(sender,**kwargs):
    # get instance of the saved-model and 
    # pass its image_id to background-tasks
    instance = kwargs.get('instance')
    print("Scheduling image saving for image id ",instance.pk,"[in signals.py]")
    save_image_encodings(instance.pk)