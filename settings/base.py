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
    'social.apps.django_app.default',
    'djcelery',
)

MY_APPS = (
    'core',
    'profiles',
    'tours',
    'shifts',
    'public',
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

AUTHENTICATION_BACKENDS = (
  #'social.backends.open_id.OpenIdAuth',
  'social.backends.google.GoogleOAuth2',
  'social.backends.username.UsernameAuth',
  'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_SECRET')


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)


############################################################
##### EMAIL ################################################
############################################################

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SERVER_EMAIL = "crimsonkeysociety@gmail.com"

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
SECRET_KEY = os.environ.get('SECRET_KEY')
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
##### CELERY ###############################################
############################################################

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = os.environ.get('CLOUDAMQP_URL')
CELERY_RESULT_DBURI = os.environ.get('DATABASE_URL')

############################################################
##### TESTS ################################################
############################################################

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

############################################################
##### SEMESTER #############################################
############################################################

# in form (month, date)
FALL_SEMESTER_START = (6, 1)
FALL_SEMESTER_END = (12, 31)

SPRING_SEMESTER_START = (1, 1)
SPRING_SEMESTER_END = (5, 31)

SEMESTER_START = {}
SEMESTER_END = {}

SEMESTER_START['fall'] = FALL_SEMESTER_START
SEMESTER_END['fall'] = FALL_SEMESTER_END
SEMESTER_START['spring'] = SPRING_SEMESTER_START
SEMESTER_END['spring'] = SPRING_SEMESTER_END

############################################################
##### OTHER SETTINGS #######################################
############################################################

VALID_HARVARD_DOMAINS = ('college.harvard.edu',)

BOARD_POSITIONS = (
    'Tour Coordinator (Primary)',
    'Treasurer',
    'Tour Coordinator',
    'Vice President',
    'President',
    'Freshman Week Coordinator',
    'Other Board Member',
    'Secretary'
)


# put these two lines at the very bottom of the settings file
import djcelery
djcelery.setup_loader()
