# coding=utf-8

"""
Django settings for ensanche project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
from distutils.sysconfig import get_python_lib

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=itf6(xf55k$lyjhog!7ng@w4(dz856x7h&pe=_)+lfr6kg1+y'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR,"vidascontadas")
SITE_ROOT           = os.path.join(PROJECT_ROOT, 'site')
APPS_ROOT        = os.path.join(PROJECT_ROOT, 'apps')
SITEPACKAGES_ROOT   = get_python_lib()
SITE_ID = 1
DEFAULT_CHARSET = 'utf-8'

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APPS_ROOT)

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

ALLOWED_HOSTS = ['*',]

# Application definition

INSTALLED_APPS = [
    #
    'filer',
    'suit',
    'registration', 
    #
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #
    'cms',
    'menus',
    'hvad',
    'treebeard',
    'datetimewidget',
    'adminsortable',
    'cicu',    
    'redactor',
    'mptt',
    'easy_thumbnails',
    'minicms',
    "categories",
    "categories.editor", 
    'pagination', 
    'el_pagination', 
    'geoposition', 
    'watson',
    'django_extensions',
    #
    'asociacion',
    'comercios',
    'victimas',
    'document_library',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'asociacion.context_processors.areacomercial',
            ],
            'debug': True,
        },
    },
]


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
    'watson.middleware.SearchContextMiddleware',

)

ROOT_URLCONF = 'vidascontadas.urls'

WSGI_APPLICATION = 'vidascontadas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE':'django.db.backends.mysql',
#        'NAME': 'ensanche',
#        'USER': 'root',
#        'PASSWORD': 'root',
#        'HOST': '',
#        'PORT': '5432',
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'
LANGUAGES = ( ('es',u"Español",),)

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(SITE_ROOT,"static")
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(SITE_ROOT,"media")
MEDIA_URL = '/media/'

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                        "django.contrib.staticfiles.finders.AppDirectoriesFinder")

STATICFILES_DIRS = (
    ('js',os.path.join(STATIC_ROOT,"js"),),
    ('images',os.path.join(STATIC_ROOT,"images"),),
    ('css',os.path.join(STATIC_ROOT,"css"),),
    ('img',os.path.join(STATIC_ROOT,"img"),),    
)

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',    
    'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
)

LANGUAGE_CODE = 'es'
DATE_FORMAT = "d/m/Y"
TIME_FORMAT = "H:i"

#CATEGORIES_SETTINGS = {
#    'M2M_REGISTRY': {
#        'comercios.asociado': 'categorias',       
#    },
#}

LOGIN_REDIRECT_URL = '/mis-comercios/'


SUIT_CONFIG = {
    'ADMIN_NAME': 'Administración Vidas Contadas',
} 


GEOPOSITION_GOOGLE_MAPS_API_KEY = "AIzaSyC1fqPCRXitBy3iFzc6hMAuB1WKLpN08vA"

try:
    from vidascontadas.local_settings import *
except:
    pass
