from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import views as auth_views
from userDB.models import *

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class SSHKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = SSHKey
        fields = ('key', 'key_type', 'hash_md5')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all()
    serializer_class = SSHKeySerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sshkeys', SSHKeyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/login/', auth_views.login, name="login"),
    url(r'accounts/logout/', auth_views.logout_then_login, name="logout"),
    url(r'^', include('userDB.urls')),
]
