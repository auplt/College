"""
Configuration for timetable app.
"""

from django.apps import AppConfig


class TimeTableConfig(AppConfig):
    """
    Class that configures timetable app for college project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timetable'
