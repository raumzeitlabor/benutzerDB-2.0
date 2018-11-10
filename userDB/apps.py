from django.apps import AppConfig
from benutzerDB import settings


class UserdbConfig(AppConfig):
    name = 'userDB'

    def ready(self):
        from django.contrib.auth.models import User
        # XXX: this errors if the db is not initialized.
        # TODO: find a way around this
        #if not User.objects.filter(username=settings.PINPAD_USERNAME).exists():
            #pinpad_user = User.objects.create_superuser(
                #username=settings.PINPAD_USERNAME,
                #password=settings.PINPAD_PASSWORD,
                #email="pinpad@tuer.rzl")
