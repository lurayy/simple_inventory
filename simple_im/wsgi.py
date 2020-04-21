"""
WSGI config for simple_im project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# from my_project import MyWSGIApp

application = get_wsgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_im.settings')
application = WhiteNoise(application, root='/staticfiles')
# application.add_files('/path/to/more/static/files', prefix='more-files/')



# application = get_wsgi_application()
