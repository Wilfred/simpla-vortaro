import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vilfredo Hjuz', 'yowilfred@gmail.com'),
)

MANAGERS = ADMINS

PROJECT_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'word_db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['simplavortaro.org', 'localhost', '127.0.0.1', '[::1]']

WSGI_APPLICATION = "wsgi.application"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'eo'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/resources/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '57-4u2^ad_udjwzo163p3x#!_wre!wyh)88mtqh79fqe-e05zq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    # django apps
    'django.contrib.staticfiles',

    # our apps
    'vortaro',

    # third party apps
    'django_nose',
    'corsheaders',
)

CORS_ORIGIN_ALLOW_ALL = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

try:
    from live_settings import *
except ImportError:
    pass
