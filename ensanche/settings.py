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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR,"ensanche")
SITE_ROOT           = os.path.join(PROJECT_ROOT, 'site')
APPS_ROOT        = os.path.join(PROJECT_ROOT, 'apps')
SITEPACKAGES_ROOT   = get_python_lib()

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APPS_ROOT)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=itf6(xf55k$lyjhog!7ng@w4(dz856x7h&pe=_)+lfr6kg1+y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'redactor',
    'south',
    'slideshow',
    'comercios',
    'filer',
    'easy_thumbnails',
    'swingtime',
    'minicms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'ensanche.urls'

WSGI_APPLICATION = 'ensanche.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'ensanche',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '5432',
    }
}

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

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(SITE_ROOT,"media")
MEDIA_URL = '/media/'

REDACTOR_OPTIONS = {'lang': 'es'}
REDACTOR_UPLOAD = 'uploads/'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

try:
    from local_settings import *
except:
    pass

TEMPLATE_DEBUG = DEBUG