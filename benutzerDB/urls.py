from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.documentation import include_docs_urls
from django.contrib.auth import views as auth_views
from userDB.models import *


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class SSHKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SSHKey
        fields = ('profile', 'key', 'key_type', 'hash_md5')

    hash_md5 = serializers.CharField(max_length=47, read_only=True)
    key_type = serializers.CharField(max_length=30, read_only=True)


class MACAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MACAddress
        fields = ('profile', 'mac', 'hostname')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'ssh_keys', 'mac_addresses')

    user = UserSerializer()
    ssh_keys = SSHKeySerializer(many=True)
    mac_addresses = MACAddressSerializer(many=True)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all()
    serializer_class = SSHKeySerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sshkeys', SSHKeyViewSet)
router.register(r'profiles', ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include_docs_urls(title="RaumZeitPanel API")),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/login/', auth_views.LoginView.as_view(), name="login"),
    url(r'accounts/logout/', auth_views.logout_then_login, name="logout"),
    url(r'^', include('userDB.urls')),
]
