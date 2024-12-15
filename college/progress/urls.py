"""
URL configuration for progress app.
"""

from django.urls import path, re_path, register_converter
from . import views
from .converters import DateConverter

app_name = 'progress'

register_converter(DateConverter, 'date')

urlpatterns = [
]
