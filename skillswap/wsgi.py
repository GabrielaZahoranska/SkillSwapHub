"""
WSGI entry point for SkillSwap Hub deployments.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

application = get_wsgi_application()
