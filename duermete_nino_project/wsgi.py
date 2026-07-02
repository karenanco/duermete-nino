"""
WSGI config for duermete_nino_project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "duermete_nino_project.settings")

application = get_wsgi_application()
