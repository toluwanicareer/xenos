"""
Django settings for xenos project.

Generated by 'django-admin startproject' using Django 1.10.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '25yq%t7r_739hj3q@c!&ov$sw+19)2z-v*9g0s*v7%joczh_e('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
'tolucareer.pythonanywhere.com',
'localhost',
'xenostrading.co',
'www.xenostrading.co',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    "account",
    "acc",
    'xenos_admin',
    "django.contrib.sites",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = 'xenos.urls'

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
                 "account.context_processors.account",
            ],
        },
    },
]

WSGI_APPLICATION = 'xenos.wsgi.application'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # During development only
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'myschoolrents@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'myschoolrents@gmail.com'
EMAIL_HOST_PASSWORD = 'test123321'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # During development only
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'myschoolrents@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'myschoolrents@gmail.com'
EMAIL_HOST_PASSWORD = 'test123321'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'xenos_prod',
        'USER': 'xenos',
        'PASSWORD': 'xenos123321',
        'HOST': 'localhost',
        'PORT': '',
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False

ACCOUNT_EMAIL_CONFIRMATION_EMAIL=False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGIN_REDIRECT_URL = '/'
SITE_ID = 1 
ACCOUNT_LOGIN_REDIRECT_URL='/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOAD_TO = os.path.join(BASE_DIR, 'media/upload')