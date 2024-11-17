"""
Configuration for user app.
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Class that configures user app for college project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
