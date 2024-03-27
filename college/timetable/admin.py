from django.contrib import admin

# Register your models here.

from .models import Student
from .models import FinalGrade


class MarksAdminSite(admin.ModelAdmin):
    model=FinalGrade
    fields = ['is_final', 'scale_100']
    list_display = ('is_final', 'scale_100', 'scale_5', 'scale_word', 'scale_letter')


admin.site.register(Student)
admin.site.register(FinalGrade, MarksAdminSite)
