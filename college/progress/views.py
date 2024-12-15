"""
Views for progress app.
"""

import copy
from ast import literal_eval
from datetime import datetime, timedelta, date
from itertools import groupby
from django.urls import reverse, resolve, Resolver404
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from psycopg2.errors import UniqueViolation

from .forms import AttendanceChooseForm
from .tables import SATable

from user.models import Student, Tutor
from group.models import GroupMember
from curriculum.models import Curriculum, CurriculumLesson, TypesOfLesson
from timetable.models import TTLesson
from .models import FinalGrade, File, Homework, StudentAttendance, Coefficient, Grade, StudentProgress


# STUDENT ATTENDANCE BLOCK

def student_attendance_choose(request, tt_lesson_id):
    """
    View for editing timetable lesson information.
    :param request: user's request
    :param user_id: user identifier
    :param curriculum_lesson_id: curriculum_lesson identifier
    :return: HTTP response HTML page with form to edit timetable lesson information or redirect page
    """
    return render(request, 'student_attendance/tt_lesson_form.html', context=context)

def student_attendance_edit(request, tt_lesson_id):
    """
    View for editing timetable lesson information.
    :param request: user's request
    :param user_id: user identifier
    :param curriculum_lesson_id: curriculum_lesson identifier
    :return: HTTP response HTML page with form to edit timetable lesson information or redirect page
    """
    tt_lesson_obj = get_object_or_404(TTLesson, tt_lesson_id=tt_lesson_id)
    tt_lesson_obj.date = tt_lesson_obj.date.strftime("%d.%m.%Y")
    tt_lesson_form = AttendanceChooseForm(request.POST or None, instance=tt_lesson_obj)
    
    return render(request, 'student_attendance/tt_lesson_form.html', context=context)





