import os
import config.py314_patch  # noqa: E402  Python 3.14 compat
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
