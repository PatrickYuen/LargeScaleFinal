"""
Django settings for LocalNotes project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GEOIP_PATH = os.path.join(BASE_DIR, "LocalNotes/GeoLite2-City.mmdb")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&lcse=6lp@zuv4gtnv#((dr^gqq_v!fm=xtewor24ixg9ooeur'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

LOGIN_URL = '/noteboard/login/'
LOGIN_REDIRECT_URL = '/search'

# Application definition

INSTALLED_APPS = [
	'noteboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LocalNotes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ "noteboard/templates" ],
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

WSGI_APPLICATION = 'LocalNotes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#putting passwords in here hardcoded probably a bad idea
DATABASES = {
	'default': {
	},
	'authdb': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'authdb',
		'USER': 'root',
		'PASSWORD': 'Inviciljigen1!',
		'HOST': '127.0.0.1',
		'PORT': '3306',
	},
	'db1': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'largescale',
		'USER': 'root',
		'PASSWORD': 'Inviciljigen1!',
		'HOST': '127.0.0.1',
		'PORT': '3306',
	},
	'db2': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'largescale2',
		'USER': 'root',
		'PASSWORD': 'Inviciljigen1!',
		'HOST': '127.0.0.1',
		'PORT': '3306',
	},
}

DATABASE_ROUTERS = ['noteboard.routers.CityRouter']


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '52.23.228.83:11211',
        ]
    }
}
