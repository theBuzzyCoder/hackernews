import os
import django


def setupDjango():
    """
    This is so that we can use Django models outside of django.
    Without this you cannot load any of the django models.
    """
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'frontend.website.settings'
    )
    django.setup()
