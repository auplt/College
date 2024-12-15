"""
Configuration for timetable app models on admin panel.
"""

from django.contrib import admin

from .models import FinalGrade


class MarksAdminSite(admin.ModelAdmin):
    """
    Class for custom configuration for models.
    """
    model = FinalGrade
    fields = ['grade_type', 'scale_100']
    list_display = ('grade_type', 'scale_100', 'scale_5', 'scale_word', 'scale_letter')


admin.site.register(FinalGrade, MarksAdminSite)
