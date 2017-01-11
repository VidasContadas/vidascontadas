import os, sys, site

site.addsitedir('/home/serendipity/webapps/areacomercial_django/env/lib/python3.3/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ensanche.settings'

activate_this = os.path.expanduser("~/webapps/areacomercial_django/env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/serendipity/webapps/areacomercial_django/ensanche/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path = ['/home/serendipity/webapps/areacomercial_django/ensanche', '/home/serendipity/webapps/areacomercial_django/ensanche/apps', '/home/serendipity/webapps/areacomercial_django'] + sys.path

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
