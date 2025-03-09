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

from .forms import HomeworkRegisterForm

from user.models import Student, Tutor
from group.models import GroupMember
from curriculum.models import Curriculum, CurriculumLesson, TypesOfLesson
from timetable.models import TTLesson
from .models import FinalGrade, File, Homework, StudentAttendance, Coefficient, Grade, StudentProgress


# HOMEWORK BLOCK

@permission_required('progress.change_homework', raise_exception=True)
def homeworks_edit(request, hw_id):
    """
    View for editing homework information.
    :param request: user's request
    :param hw_id: homework entity identifier
    :return: HTTP response HTML page with form to edit homework information or redirect page
    """
    homework_obj = get_object_or_404(Homework, hw_id=hw_id)
    homework_form = HomeworkRegisterForm(request.POST or None, instance=homework_obj)
    if homework_form.is_valid():
        homework_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'домашнее задание'
        request.session["obj_action"] = 'U'
        try:
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('progress:homework_details', kwargs={'hw_id': hw_id}))
    context = {'homework_form': homework_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'homework/homework_form.html', context=context)


