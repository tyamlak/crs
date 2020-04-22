from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CriminalImage,ImageEncoding


@receiver(post_save,sender=CriminalImage)
def train_image(sender,**kwargs):
    # get instance of the saved-model and save
    # the trained-model in pkl format
    pass