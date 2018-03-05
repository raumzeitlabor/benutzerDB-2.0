from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils import translation
from . import models


@login_required
def index(request):
    return render(request, "index.html")


class SSHKeyView(ListView):
    queryset = models.SSHKey.objects.all()
    template_name = 'sshkey_list.html'


class MACAddressView(ListView):
    queryset = models.MACAddress.objects.all()
    template_name = 'macaddress_list.html'


def switch_language(request, language):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if hasattr(request, 'session'):
        request.session[LANGUAGE_SESSION_KEY] = language
    else:
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )

    return response
