import os
import sys

sys.path = ['/home/serendipity/webapps/ensanche_django', '/home/serendipity/webapps/ensanche_django/lib/python2.7'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'ensanche.settings'
application = WSGIHandler()
