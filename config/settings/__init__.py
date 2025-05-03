"""
Settings initialization.
"""

import os

# Set the default settings module
environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *
