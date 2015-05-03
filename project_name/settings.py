# -*- coding: utf-8 -*-

import os

from yaml import load as yaml_load
try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

from django.core.exceptions import ImproperlyConfigured


########################################################################################################################
# Helpers
########################################################################################################################


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the %s env variable" % setting)


########################################################################################################################
# Global Paths
########################################################################################################################


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


########################################################################################################################
# Load settings from yaml config
########################################################################################################################


__YAML_SETTING_FILENAME = get_env_setting('{{ project_name }}.yml')
if not os.path.isfile(__YAML_SETTING_FILENAME):
    raise ImproperlyConfigured("File %s not found." % __YAML_SETTING_FILENAME)

try:
    __YAML_SETTING = yaml_load(file(__YAML_SETTING_FILENAME, 'r'), Loader=YamlLoader)
except Exception as e:
    raise ImproperlyConfigured("Error loading file %s. %s" % (__YAML_SETTING_FILENAME, e))


########################################################################################################################
# Consts
########################################################################################################################


SECRET_KEY = '{{ secret_key }}'

DEBUG = TEMPLATE_DEBUG = __YAML_SETTING['project'].get('debug', False)

ALLOWED_HOSTS = []

STATIC_URL = __YAML_SETTING['project']['static_url']
STATIC_ROOT = __YAML_SETTING['project']['static_root']


########################################################################################################################
# Locale, encoding, time
########################################################################################################################


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = __YAML_SETTING['project'].get('language_code', 'en-us')

TIME_ZONE = __YAML_SETTING['project'].get('timezone', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


########################################################################################################################
# Databases and other storage
########################################################################################################################


__DATABASE_ENGINE_MAP = {
    'mysql': 'django.db.backends.mysql'
}

DATABASES = {}
for __name, __settings in __YAML_SETTING['database'].iteritems():
    if __settings['engine'] not in __DATABASE_ENGINE_MAP:
        raise ImproperlyConfigured('Database engine %s not found.' % __settings['engine'])

    DATABASES.update({
        __name: {
            'ENGINE': __DATABASE_ENGINE_MAP[__settings['engine']],
            'NAME': __settings['name'],
            'USER': __settings['user'],
            'PASSWORD': __settings['password'],
            'HOST': __settings['host'],
        }
    })


########################################################################################################################
# Applications
########################################################################################################################


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    '{{ project_name }}'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
