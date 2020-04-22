from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = 'UserProfile'

    def ready(self):
        from .signals import train_image
