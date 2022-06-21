import os
import sys

import django


def pytest_configure(config):
    sys.path.insert(0, '/Users/grantjenks/repos/django-replay/tests')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'
    django.setup()
