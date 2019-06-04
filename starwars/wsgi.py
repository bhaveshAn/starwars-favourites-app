"""
WSGI config for starwars project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# Use heroku platform if not set
platform = os.getenv("STARWARS_PLATFORM", "heroku")

if platform == "dev":
    settings = "starwars.settings.dev"
elif platform == "heroku":
    settings = "starwars.settings.heroku"
else:
    settings = "starwars.settings.prod"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()

# Use WhiteNoise to serve static assets on heroku
if platform == "heroku":
    application = DjangoWhiteNoise(application)
