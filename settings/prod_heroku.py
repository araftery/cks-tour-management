from base import *

############################################################
##### STATIC FILES #########################################
############################################################

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


############################################################
##### DATABASE #############################################
############################################################

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()
CELERY_RESULT_DBURI = DATABASES['default']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

############################################################
##### OTHER ################################################
############################################################

DEBUG = False
TEMPLATE_DEBUG = False

SETTINGS_MODULE = 'settings.prod_heroku'
