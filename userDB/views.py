from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils import translation
from django.urls import reverse_lazy
import json
from . import models


@login_required
def index(request):
    return render(request, "index.html")

@user_passes_test(lambda u: u.is_superuser)
def pinpad_pinlist(request):
    '''List all pins.

    This view is only meant to be used by the Pinpad and exists for
    compatibility with the old BenutzerDB. It should eventually be removed once
    the Pinpad has been migrated to use the new API.
    '''
    members = models.Profile.objects.filter(member=True)
    pinlist = {member.user.get_username(): str(member.pin)
               for member in members}
    data = json.dumps(pinlist)
    print(data)
    return HttpResponse(data, content_type='application/json')


class SSHKeyView(ListView):
    queryset = models.SSHKey.objects.all()
    template_name = 'sshkey_list.html'


class SSHKeyCreate(CreateView):
    model = models.SSHKey
    fields = ['name', 'key']
    template_name = 'sshkey_form.html'
    success_url = reverse_lazy('ssh-keys-list')

    def form_valid(self, form):
        form.instance.profile_id = self.request.user.profile.id
        return super().form_valid(form)

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
