from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = 'UserProfile'

    def ready(self):
        from .signals import schedule_image_encoding
