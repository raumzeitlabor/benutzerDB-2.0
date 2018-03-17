benutzerDB
==========

Die neue RZL benutzerDB. Jetzt in Django.

Installation
------------

* virtualenvironment anlegen
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py createsuperuser
* python manage.py runserver

CoreAPI
-------

Das Django REST Framework, auf dem die BenutzerDB basiert,  verwendet
[CoreAPI](http://www.coreapi.org/) und hat autogenerierte Dokumentation. Diese
kann unter $URL/docs/ gefunden werden. Desweiteren kann via dem coreapi-cli (pip
install coreapi-cli) Client mit der API interagiert werden.
