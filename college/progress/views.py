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


from user.models import Student, Tutor
from group.models import GroupMember
from curriculum.models import Curriculum, CurriculumLesson, TypesOfLesson
from timetable.models import TTLesson
from .models import FinalGrade, File, Homework, StudentAttendance, Coefficient, Grade, StudentProgress


# STUDENT ATTENDANCE BLOCK







