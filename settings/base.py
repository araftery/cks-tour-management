import os

from path import path

############################################################
##### SETUP ################################################
############################################################

# i.e., where root urlconf is
PROJECT_ROOT = path(__file__).abspath().dirname().dirname()


############################################################
##### DATABASE #############################################
############################################################

ALLOWED_HOSTS = ['*']

############################################################
##### APPS #################################################
############################################################

# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'crispy_forms',
    'selectize',
)

MY_APPS = (
    'core',
    'profiles',
    'tours',
    'shifts',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + MY_APPS

############################################################
##### MIDDLEWARE ###########################################
############################################################

DEFAULT_MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

THIRD_PARTY_MIDDLEWARE = (
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

############################################################
##### INTERNATIONALIZATION #################################
############################################################

LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
INTERNAL_IPS = ['*']

############################################################
##### TEMPLATES ############################################
############################################################

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TCP

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
) + DEFAULT_TCP


############################################################
##### AUTHENTICATION #######################################
############################################################

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''

############################################################
##### EMAIL ################################################
############################################################

# MANDRILL_USER = os.environ.get('MANDRILL_USER')
# MANDRILL_API_KEY = os.environ.get('MANDRILL_API_KEY')
# EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
# SERVER_EMAIL = "quadgrill@quadgrill.com"

ADMINS = (
    ('Andrew Raftery', 'andrewraftery@gmail.com'),
)

############################################################
##### STATIC FILES #########################################
############################################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_common').replace('\\','/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


############################################################
##### OTHER ################################################
############################################################

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
SECRET_KEY = 'ye#fv=lsp5sm@4lg@23(55d64qydp1%=2)wdkr!twr5_827g8n'
DATABASES = {}
TIME_ZONE = 'America/New_York'
USE_TZ = True
SITE_ID = 1

# BUGSNAG = {
#  "api_key": os.environ.get('BUGSNAG_API_KEY'),
#  "project_root": "/app",
# }

############################################################
##### CRISPY FORMS #########################################
############################################################

CRISPY_TEMPLATE_PACK = 'bootstrap3'


############################################################
##### TWILIO ###############################################
############################################################
# TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
# TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
# TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')


############################################################
##### CELERY ###############################################
############################################################

# CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# BROKER_URL = os.environ.get('CLOUDAMQP_URL')
# CELERY_RESULT_DBURI = os.environ.get('DATABASE_URL')

# put these two lines at the very bottom of the settings file
# import djcelery
# djcelery.setup_loader()

############################################################
##### TESTS ################################################
############################################################

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

############################################################
##### SEMESTER #############################################
############################################################

# in form (month, date)
FALL_SEMESTER_START = (8, 1)
FALL_SEMESTER_END = (12, 31)

SPRING_SEMESTER_START = (1, 1)
SPRING_SEMESTER_END = (7, 31)

SEMESTER_START = {}
SEMESTER_END = {}

SEMESTER_START['fall'] = FALL_SEMESTER_START
SEMESTER_END['fall'] = FALL_SEMESTER_END
SEMESTER_START['spring'] = SPRING_SEMESTER_START
SEMESTER_END['spring'] = SPRING_SEMESTER_END

############################################################
##### OTHER SETTINGS #######################################
############################################################

DEFAULT_NUM_TOURS_SETTING_NAME = 'Tours Required'
DEFAULT_NUM_SHIFTS_SETTING_NAME = 'Shifts Required'
