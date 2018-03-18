from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.utils import translation
from django.urls import reverse_lazy
from django.conf import settings
import urllib
import ipaddress
import requests
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
    pinlist = [{"handle": member.user.get_username(), "pin": str(member.pin)}
               for member in members]
    # The JSON should be sorted to ensure that the CRC which is calculated by
    # the pinpad-controller on every sync  does not change if no PINs have
    # changed.
    data = json.dumps(pinlist, sort_keys=True)
    return HttpResponse(data, content_type='application/json')


@method_decorator(login_required, name='dispatch')
class SSHKeyView(ListView):
    template_name = 'sshkey_list.html'

    def get_queryset(self):
        return models.SSHKey.objects.filter(profile=self.request.user.profile)


@method_decorator(login_required, name='dispatch')
class SSHKeyCreate(CreateView):
    model = models.SSHKey
    fields = ['name', 'key']
    template_name = 'sshkey_form.html'
    success_url = reverse_lazy('ssh-keys-list')

    def form_valid(self, form):
        form.instance.profile_id = self.request.user.profile.id
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SSHKeyDelete(DeleteView):
    success_url = reverse_lazy('ssh-keys-list')
    template_name = 'sshkey_confirm_delete.html'

    def get_queryset(self):
        return models.SSHKey.objects.filter(profile=self.request.user.profile)


@method_decorator(login_required, name='dispatch')
class MACAddressView(ListView):
    template_name = 'macaddress_list.html'

    def get_queryset(self):
        return models.MACAddress.objects.filter(profile=self.request.user.profile)


def get_ip_details(ip):
    # FIXME: Error handling
    api_base = getattr(settings, 'UNIFI_CONTROLLER_HOST')
    api_login = {
        'username': getattr(settings, 'UNIFI_CONTROLLER_USER'),
        'password': getattr(settings, 'UNIFI_CONTROLLER_PASS'),
    }

    s = requests.Session()
    r = s.post('{}/api/login'.format(api_base), json=api_login, verify=False)
    r = s.get('{}/api/s/default/stat/sta'.format(api_base))

    clients = r.json()
    clients = list(filter(lambda c: c['ip'] == ip, clients['data']))

    if not clients or len(clients) > 1:
        return None

    return clients[0]


@method_decorator(login_required, name='dispatch')
class MACAddressCreate(CreateView):
    model = models.MACAddress
    fields = ['hostname']
    template_name = 'macaddress_form.html'
    success_url = reverse_lazy('mac-addresses-list')

    def form_valid(self, form):
        form.instance.profile_id = self.request.user.profile.id
        client_ip = self.request.META.get('REMOTE_ADDR')

        if not ipaddress.ip_address(client_ip) in ipaddress.ip_network('172.22.36.0/23'):
            raise ValidationError(_('You need to be in one of the RaumZeitLabor wifi networks to add your MAC address.'))

        client = get_ip_details(client_ip)
        if not client:
            return ValidationError('Could not find client in Ubiquiti controller API json')

        form.instance.mac = client['mac']
        form.instance.vendor = client['oui']
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        client_ip = self.request.META.get('REMOTE_ADDR')
        client = get_ip_details(client_ip)

        if client:
            context['ubiquiti_client'] = client

        return context


@method_decorator(login_required, name='dispatch')
class MACAddressDelete(DeleteView):
    success_url = reverse_lazy('mac-addresses-list')
    template_name = 'macaddress_confirm_delete.html'

    def get_queryset(self):
        return models.MACAddress.objects.filter(profile=self.request.user.profile)


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
