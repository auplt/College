"""
Views for timetable app.
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

from .forms import TTLessonRegisterForm, LessonTimeRegisterForm, ClassroomRegisterForm

from group.models import GroupMember
from curriculum.models import CurriculumLesson, TypesOfLesson
from .models import Classroom, TTLesson, LessonTime


# CLASSROOM BLOCK

def classroom_list(request):
    """
    View for list of classrooms.
    :param request: user's request
    :return: HTTP response HTML page with classrooms list
    """
    classrooms = Classroom.objects.order_by('number').all()
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context = {'classrooms': classrooms}
    context.update(obj_stats)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_list.html', context=context)


def classroom_details(request, classroom_id):
    """
    View for classroom details.
    :param request: user's request
    :param classroom_id: classroom identifier
    :return: HTTP response HTML page with classroom details
    """
    classroom_obj = Classroom.objects.get(classroom_id=classroom_id)
    context = {'classroom': classroom_obj}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    context.update(tt_lesson_details(request, classroom_id=classroom_id))
    print(context)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_details.html', context=context)


@permission_required('timetable.add_classroom', raise_exception=True)
def classroom_register(request):
    """
    View for classroom registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register classroom or redirect page
    """
    if request.method == 'POST':
        classroom_form = ClassroomRegisterForm(request.POST)
        if classroom_form.is_valid():
            new_classroom = classroom_form.save(commit=False)
            new_classroom.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'аудитория'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:classroom_list'))
    else:
        classroom_form = ClassroomRegisterForm()
    context = {'classroom_form': classroom_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_form.html', context=context)


@permission_required('timetable.change_classroom', raise_exception=True)
def classroom_edit(request, classroom_id):
    """
    View for editing classroom information.
    :param request: user's request
    :param classroom_id: classroom identifier
    :return: HTTP response HTML page with form to edit classroom information or redirect page
    """
    classroom_obj = get_object_or_404(Classroom, classroom_id=classroom_id)
    print(classroom_obj)
    classroom_form = ClassroomRegisterForm(request.POST or None, instance=classroom_obj)
    if classroom_form.is_valid():
        classroom_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'аудитория'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('timetable:classroom_details', kwargs={'classroom_id': classroom_id}))
    context = {'classroom_form': classroom_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_form.html', context=context)


@permission_required('timetable.delete_classroom', raise_exception=True)
def classroom_delete(request, classroom_id):
    """
    View for deleting classroom information.
    :param request: user's request
    :param classroom_id: classroom identifier
    :return: HTTP response HTML page with form to delete classroom information or redirect page
    """
    classroom_obj = get_object_or_404(Classroom, classroom_id=classroom_id)
    if request.method == 'POST':
        request.session["obj_name"] = 'аудитория'
        request.session["obj_action"] = 'D'
        try:
            classroom_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                if resolve_match.url_name == 'classroom_details':
                    raise Http404
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:classroom_list'))
        except Http404:
            return redirect(reverse('timetable:classroom_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:classroom_details', kwargs={'classroom_id': classroom_id}))
    context = {'classroom': classroom_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_delete.html', context=context)


# LESSON TIME BLOCK

@permission_required('timetable.view_lessontime', raise_exception=True)
def lesson_time_list(request):
    """
    View for list of lessons time.
    :param request: user's request
    :return: HTTP response HTML page with lesson times list
    """
    lesson_times = LessonTime.objects.order_by('start_time', 'end_time').all()
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context = {'lesson_times': lesson_times}
    context.update(obj_stats)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_list.html', context=context)


@permission_required('timetable.view_lessontime', raise_exception=True)
def lesson_time_details(request, lesson_id):
    """
    View for lesson time details.
    :param request: user's request
    :param lesson_id: lesson time entity identifier
    :return: HTTP response HTML page with lesson time details
    """
    lesson_time = LessonTime.objects.get(lesson_id=lesson_id)
    context = {'lesson_time': lesson_time}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    print(context)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_details.html', context=context)


@permission_required('timetable.add_lessontime', raise_exception=True)
def lesson_time_register(request):
    """
    View for lesson time registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register lesson time entity or redirect page
    """
    if request.method == 'POST':
        lesson_time_form = LessonTimeRegisterForm(request.POST)
        if lesson_time_form.is_valid():
            new_lesson_time = lesson_time_form.save(commit=False)
            new_lesson_time.save()
            print(new_lesson_time)
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'время занятия'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:lesson_time_list'))
    else:
        lesson_time_form = LessonTimeRegisterForm()
    context = {'lesson_time_form': lesson_time_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_form.html', context=context)


@permission_required('timetable.change_lessontime', raise_exception=True)
def lesson_time_edit(request, lesson_id):
    """
    View for editing lesson time information.
    :param request: user's request
    :param lesson_id: lesson time entity identifier
    :return: HTTP response HTML page with form to edit lesson time information or redirect page
    """
    lesson_time_obj = get_object_or_404(LessonTime, lesson_id=lesson_id)
    lesson_time_form = LessonTimeRegisterForm(request.POST or None, instance=lesson_time_obj)
    if lesson_time_form.is_valid():
        lesson_time_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'время занятия'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('timetable:lesson_time_details', kwargs={'lesson_id': lesson_id}))
    context = {'lesson_time_form': lesson_time_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_form.html', context=context)


@permission_required('timetable.delete_lessontime', raise_exception=True)
def lesson_time_delete(request, lesson_id):
    """
    View for deleting lesson time information.
    :param request: user's request
    :param lesson_id: lesson time entity identifier
    :return: HTTP response HTML page with form to delete lesson time information or redirect page
    """
    lesson_time_obj = get_object_or_404(LessonTime, lesson_id=lesson_id)
    if request.method == 'POST':
        request.session["obj_name"] = 'время занятия'
        request.session["obj_action"] = 'D'
        try:
            lesson_time_obj.delete()
            request.session["obj_status"] = 'success'

            try:
                resolve_match = resolve(request.GET.get('next'))
                if resolve_match.url_name == 'lesson_time_details':
                    raise Http404
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:lesson_time_list'))
        except Http404:
            return redirect(reverse('timetable:lesson_time_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('timetable:lesson_time_details', kwargs={'lesson_id': lesson_id}))
    context = {'lesson_time': lesson_time_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_delete.html', context=context)


# TIMETABLE LESSON BLOCK

def tt_lesson_details(request, user_id=None, classroom_id=None, group_id=None):
    """
    Function to get timetable for users, classrooms and groups.
    :param request: user's request
    :param user_id: user identifier
    :param classroom_id: classroom identifier
    :param group_id: group identifier
    :return: dict with tt_lesson objects, grouped in appropriate way
    """
    is_week = False
    week_delta = None
    student_group_id = None
    tt_lesson_objs = []
    selected_tt_lesson_objs = []
    try:
        day_delta = int(request.GET.get('day_delta', 0))
    except TypeError:
        day_delta = 0
    start_dt = date.today() + timedelta(days=day_delta)

    day_count = 1

    if 'week' in request.GET.keys():
        try:
            is_week = eval(request.GET.get('week'))
        except NameError:
            is_week = False

    if is_week:
        try:
            week_delta = int(request.GET.get('week_delta', 0))
        except TypeError:
            week_delta = 0

        dt = date.today() + timedelta(days=week_delta * 7)
        start_dt = dt - timedelta(days=dt.weekday())
        day_count = 7

    # Getting info about all student's group_semester_ids (about student's group history (group + semester num))
    if user_id is not None:
        group_semester_ids = (GroupMember.objects.select_related('student_id__user_id')
                              .filter(student_id__user_id=user_id)
                              .values('group_semester_id')
                              .all())
    else:
        group_semester_ids = None

    for dt in [d for d in (start_dt + timedelta(n) for n in range(day_count))]:
        # Case for classroom
        if classroom_id is not None:
            obj = (TTLesson.objects
                   .filter(date=dt, classroom_id=classroom_id)
                   .order_by('date',
                             'day_name',
                             'week_type',
                             'lesson_time_id__lesson_id',
                             'lesson_time_id__start_time',
                             'lesson_time_id__end_time',
                             'classroom_id__classroom_id',
                             'classroom_id__number',
                             'curriculum_lesson_id__lesson_type',
                             'curriculum_lesson_id__curriculum_id__discipline_id__discipline_id',
                             'curriculum_lesson_id__curriculum_id__discipline_id__name'))

            print(obj)

        # Case for group
        elif group_id is not None:
            # Searching for tt_lesson's identifiers (day_name, week_type, lesson_time_id) to get whole info about
            # all groups, tutors, etc. involved in the lesson
            tt_lessons = (TTLesson.objects
                          .select_related('curriculum_lesson_id__curriculum_id__group_semester_id__group_id')
                          .filter(date=dt,
                                  curriculum_lesson_id__curriculum_id__group_semester_id__group_id=group_id)
                          .values('day_name', 'week_type', 'curriculum_lesson_id', 'lesson_time_id'))
            day_name_list = [tt_lesson_id['day_name'] for tt_lesson_id in tt_lessons]
            week_type_list = [tt_lesson_id['week_type'] for tt_lesson_id in tt_lessons]
            lesson_time_id_list = [tt_lesson_id['lesson_time_id'] for tt_lesson_id in tt_lessons]
            obj = (TTLesson.objects
                   .filter(date=dt,
                           day_name__in=day_name_list,
                           week_type__in=week_type_list,
                           lesson_time_id__in=lesson_time_id_list)
                   .order_by('date',
                             'day_name',
                             'week_type',
                             'lesson_time_id__lesson_id',
                             'lesson_time_id__start_time',
                             'lesson_time_id__end_time',
                             'classroom_id__classroom_id',
                             'classroom_id__number',
                             'curriculum_lesson_id__lesson_type',
                             'curriculum_lesson_id__curriculum_id__discipline_id__discipline_id',
                             'curriculum_lesson_id__curriculum_id__discipline_id__name'))

        # Case for users (tutors & students)
        elif user_id is not None:
            student_group_id = (GroupMember.objects
                                .select_related('student_id__user_id__id',
                                                'group_semester_id')
                                .values('group_semester_id__group_id')
                                .order_by('-group_semester_id__semester_num')
                                .first())
            if student_group_id:
                student_group_id = student_group_id['group_semester_id__group_id']

            # Searching for tt_lesson's identifiers (day_name, week_type, lesson_time_id) related to tutor
            # to get whole info about all groups, tutors, etc. involved in the lesson
            tt_lesson_tutor = \
                (TTLesson.objects
                 .select_related('curriculum_lesson_id__tutor_id__user_id')
                 .filter(date=dt,
                         curriculum_lesson_id__tutor_id__user_id=user_id)
                 .values('day_name', 'week_type', 'curriculum_lesson_id', 'lesson_time_id'))

            # Searching for tt_lesson's identifiers (day_name, week_type, lesson_time_id) related to student
            # to get whole info about all groups, tutors, etc. involved in the lesson
            tt_lesson_student = \
                (TTLesson.objects
                 .select_related('curriculum_lesson_id__curriculum_id')
                 .filter(date=dt,
                         curriculum_lesson_id__curriculum_id__group_semester_id__in=group_semester_ids)
                 .values('day_name', 'week_type', 'curriculum_lesson_id', 'lesson_time_id'))

            tt_lesson_ids = tt_lesson_tutor.union(tt_lesson_student)
            day_name_list = [tt_lesson_id['day_name'] for tt_lesson_id in tt_lesson_ids]
            week_type_list = [tt_lesson_id['week_type'] for tt_lesson_id in tt_lesson_ids]
            lesson_time_id_list = [tt_lesson_id['lesson_time_id'] for tt_lesson_id in tt_lesson_ids]
            obj = (TTLesson.objects
                   .filter(date=dt,
                           day_name__in=day_name_list,
                           week_type__in=week_type_list,
                           lesson_time_id__in=lesson_time_id_list)
                   .order_by('date',
                             'day_name',
                             'week_type',
                             'lesson_time_id__lesson_id',
                             'lesson_time_id__start_time',
                             'lesson_time_id__end_time',
                             'classroom_id__classroom_id',
                             'classroom_id__number',
                             'curriculum_lesson_id__lesson_type',
                             'curriculum_lesson_id__curriculum_id__discipline_id__discipline_id',
                             'curriculum_lesson_id__curriculum_id__discipline_id__name'

                             ))
        else:
            raise Http404

        # Grouping tt_lesson_objects by curriculum_lesson
        tt_lesson_obj = [
            {
                'date': list(key)[0],
                'day_name': list(key)[1],
                'week_type': list(key)[2],
                'lesson_time_id': list(key)[3],
                'start_time': list(key)[4],
                'end_time': list(key)[5],
                'classroom_id': list(key)[6],
                'classroom_number': list(key)[7],
                'lesson_type': list(key)[8],
                'discipline_id': list(key)[9],
                'discipline_name': list(key)[10],
                'lesson_info': [
                    {
                        'tutor':
                            {
                                'tt_lesson_id': item.tt_lesson_id,
                                'id': item.curriculum_lesson_id.tutor_id.user_id.id,
                                'last_name': item.curriculum_lesson_id.tutor_id.user_id.last_name,
                                'first_name': item.curriculum_lesson_id.tutor_id.user_id.first_name,
                                'second_name': item.curriculum_lesson_id.tutor_id.user_id.second_name
                            },
                        'group':
                            {
                                'tt_lesson_id': item.tt_lesson_id,
                                'group_id': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.group_id,
                                'name': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.name
                            }
                    } for item in grp
                ]
            } for key, grp in
            groupby(obj, key=lambda x: (x.date,
                                        x.day_name,
                                        x.week_type,
                                        x.lesson_time_id.lesson_id,
                                        x.lesson_time_id.start_time,
                                        x.lesson_time_id.end_time,
                                        x.classroom_id.classroom_id,
                                        x.classroom_id.number,
                                        x.curriculum_lesson_id.lesson_type,
                                        x.curriculum_lesson_id.curriculum_id.discipline_id.discipline_id,
                                        x.curriculum_lesson_id.curriculum_id.discipline_id.name,
                                        ))
        ]

        tt_lesson_objs.extend(tt_lesson_obj)

        selected_tt_lesson_objs = []

        # Remain timetable lessons where requested group takes place
        for tt_lesson_obj in tt_lesson_objs:
            if group_id:
                for les_inf in tt_lesson_obj['lesson_info']:
                    if str(les_inf['group']['group_id']) == str(group_id):
                        selected_tt_lesson_objs.append(tt_lesson_obj)
                        break
            if user_id:
                for les_inf in tt_lesson_obj['lesson_info']:
                    if (str(les_inf['tutor']['id']) == str(user_id) or
                            str(les_inf['group']['group_id']) == str(student_group_id)):
                        selected_tt_lesson_objs.append(tt_lesson_obj)
                        break

        if classroom_id:
            selected_tt_lesson_objs.extend(copy.deepcopy(tt_lesson_objs))

    # Grouping list of tt_lesson_objects by days
    tt_lesson_obj = [
        {
            'date': list(key)[0],
            'day_name': list(key)[1],
            'week_type': list(key)[2],
            'days_info': [
                {
                    'start_time': item['start_time'],
                    'end_time': item['end_time'],
                    'lesson_time_id': item['lesson_time_id'],
                    'classroom_id': item['classroom_id'],
                    'classroom_number': item['classroom_number'],
                    'lesson_type': item['lesson_type'],
                    'discipline_id': item['discipline_id'],
                    'discipline_name': item['discipline_name'],
                    'lesson_info': item['lesson_info']
                } for item in grp
            ]
        } for key, grp in groupby(selected_tt_lesson_objs, key=lambda x: (x['date'], x['day_name'], x['week_type']))
    ]

    # Sort lessons inside one day by the time they start
    for tt_lesson in tt_lesson_obj:
        tt_lesson['days_info'].sort(key=lambda d: d['start_time'])

    # Inserting missing dates to the list of dates with empty lessons list
    for n in range(day_count):
        dt = start_dt + timedelta(n)
        if len(tt_lesson_obj) <= n or tt_lesson_obj[n]['date'] != dt:
            elem = {
                'date': dt,
                'day_name': dt.strftime('%a').upper(),
                'week_type': TTLesson.get_week_type(dt),
                'days_info': []
            }
            tt_lesson_obj.insert(n, elem)

    context = {
        'tt_lessons': tt_lesson_obj,
        'lesson_types': dict(TypesOfLesson.choices),
        'week_types': dict(TTLesson.TYPE_OF_WEEK_CHOICES),
        'day_names': dict(TTLesson.DAY_OF_WEEK_CHOICES),
        'is_week': is_week,
        'week_delta': week_delta,
        'day_delta': day_delta
    }
    return context


@permission_required('timetable.change_ttlesson', raise_exception=True)
def tt_lesson_details_edit(request):
    """
    Function to watch timetable details and edit.
    :param request: user's request
    :return: HTTP response HTML page with timetables details and buttons to edit
    """
    # if 'dt' in request.GET.keys():

    is_week = False
    week_delta = None
    day_delta = None
    tt_lesson_objs = []
    try:
        # request.GET.get('dt')))
        tt_lesson_ids = request.GET.get('tt_lesson_ids')
        print(literal_eval(tt_lesson_ids))
        tt_lesson_ids_lst = literal_eval(tt_lesson_ids)

        # tt_lesson_ids_lst = [-1, 32, 34]

        obj = (TTLesson.objects
               .filter(tt_lesson_id__in=tt_lesson_ids_lst)
               .order_by('date', 'lesson_time_id__start_time'))

        print(obj)

        # Grouping tt_lesson_objects by curriculum_lesson
        tt_lesson_obj = [
            {
                'date': list(key)[0],
                'day_name': list(key)[1],
                'week_type': list(key)[2],
                'lesson_time_id': list(key)[3].lesson_id,
                'start_time': list(key)[3].start_time,
                'end_time': list(key)[3].end_time,
                'classroom_id': list(key)[4].classroom_id,
                'classroom_number': list(key)[4].number,
                'lesson_type': list(key)[5],
                'discipline_id': list(key)[6],
                'discipline_name': list(key)[7],
                'lesson_info': [
                    {
                        'tutor':
                            {
                                'tt_lesson_id': item.tt_lesson_id,
                                'id': item.curriculum_lesson_id.tutor_id.user_id.id,
                                'last_name': item.curriculum_lesson_id.tutor_id.user_id.last_name,
                                'first_name': item.curriculum_lesson_id.tutor_id.user_id.first_name,
                                'second_name': item.curriculum_lesson_id.tutor_id.user_id.second_name
                            },
                        'group':
                            {
                                'tt_lesson_id': item.tt_lesson_id,
                                'group_id': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.group_id,
                                'name': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.name
                            }
                    } for item in grp
                ]
            } for key, grp in
            groupby(obj, key=lambda x: (x.date,
                                        x.day_name,
                                        x.week_type,
                                        x.lesson_time_id,
                                        x.classroom_id,
                                        x.curriculum_lesson_id.lesson_type,
                                        x.curriculum_lesson_id.curriculum_id.discipline_id.discipline_id,
                                        x.curriculum_lesson_id.curriculum_id.discipline_id.name,
                                        ))
        ]

        tt_lesson_objs.extend(tt_lesson_obj)

        # Grouping list of tt_lesson_objects by days
        tt_lesson_obj = [
            {
                'date': list(key)[0],
                'day_name': list(key)[1],
                'week_type': list(key)[2],
                'days_info': [
                    {
                        'start_time': item['start_time'],
                        'end_time': item['end_time'],
                        'lesson_time_id': item['lesson_time_id'],
                        'classroom_id': item['classroom_id'],
                        'classroom_number': item['classroom_number'],
                        'lesson_type': item['lesson_type'],
                        'discipline_id': item['discipline_id'],
                        'discipline_name': item['discipline_name'],
                        'lesson_info': item['lesson_info']
                    } for item in grp
                ]
            } for key, grp in groupby(tt_lesson_objs, key=lambda x: (x['date'], x['day_name'], x['week_type']))
        ]

        print(tt_lesson_obj)

        # Sort lessons inside one day by the time they start
        for tt_lesson in tt_lesson_obj:
            tt_lesson['days_info'].sort(key=lambda d: d['start_time'])

        print(tt_lesson_obj)

        # Inserting missing dates to the list of dates with empty lessons list
        # for n in range(day_count):
        #     dt = start_dt + timedelta(n)
        #     if len(tt_lesson_obj) <= n or tt_lesson_obj[n]['date'] != dt:
        #         elem = {
        #             'date': dt,
        #             'day_name': dt.strftime('%a').upper(),
        #             'week_type': TTLesson.get_week_type(dt),
        #             'days_info': []
        #         }
        #         tt_lesson_obj.insert(n, elem)
        #
        context = {
            'tt_lessons': tt_lesson_obj,
            'lesson_types': dict(TypesOfLesson.choices),
            'week_types': dict(TTLesson.TYPE_OF_WEEK_CHOICES),
            'day_names': dict(TTLesson.DAY_OF_WEEK_CHOICES),
            'is_week': is_week,
            'week_delta': week_delta,
            'day_delta': day_delta
        }

        obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
        if obj_stats:
            for obj_stat in obj_stats:
                del request.session[obj_stat]
        context.update(obj_stats)
        print(context)
        if 'next' in request.GET.keys():
            context['next_url'] = request.GET.get('next')

        print(1123)

        return render(request, 'tt_lesson/tt_lesson_details_edit.html', context=context)
        # return render(request, 'group/group_list.html', context=context)


    except TypeError:
        raise Http404
        # print(18)


@permission_required('timetable.add_ttlesson', raise_exception=True)
def tt_lesson_register(request):
    """
    View for timetable lesson registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register timetable lesson or redirect page
    """
    if request.method == 'POST':
        tt_lesson_form = TTLessonRegisterForm(request.POST)
        if tt_lesson_form.is_valid():
            new_tt_lesson = tt_lesson_form.save(commit=False)
            new_tt_lesson.set_day_name(tt_lesson_form.cleaned_data['date'])
            new_tt_lesson.set_week_type(tt_lesson_form.cleaned_data['date'])
            try:
                new_tt_lesson.save()
                request.session["obj_status"] = 'success'
                request.session["obj_name"] = 'занятие в расписании'
                request.session["obj_action"] = 'C'
                try:
                    resolve_match = resolve(request.GET.get('next').split('?')[0])
                    return redirect(request.GET.get('next').replace(':', '&'))
                except Resolver404 or KeyError:
                    return redirect(reverse('group:group_list'))
            except IntegrityError as ex:
                if isinstance(ex.__cause__, UniqueViolation):
                    if ex.__cause__.diag.constraint_name == 'tt_lesson_day_week_time_curriculum_les_unique':
                        tt_lesson_form.add_error(None, "У группы уже есть занятие в это время")
                else:
                    tt_lesson_form.add_error(None, ex.__cause__)
    else:
        curriculum_lesson_objects = None
        initial = {}
        if 'date' in request.GET.dict():
            print(request.GET.get('date'))
            initial['date'] = request.GET.get('date')
        if 'lesson_time_id' in request.GET.dict():
            print(request.GET.get('lesson_time_id'))
            initial['lesson_time_id'] = request.GET.get('lesson_time_id')
        if initial:
            tt_lesson_form = TTLessonRegisterForm(initial=initial)
        else:
            tt_lesson_form = TTLessonRegisterForm()

        if 'classroom_id' in request.GET.dict() and 'tutor_ids' in request.GET.dict():
            print(request.GET.get('tutor_ids'))
            tutor_ids = literal_eval(request.GET.get('tutor_ids'))
            classroom_obj = get_object_or_404(Classroom, classroom_id=request.GET.get('classroom_id'))
            initial['classroom_id'] = classroom_obj
            tt_lesson_form = TTLessonRegisterForm(initial=initial)

            if 'date' in request.GET.dict() and 'lesson_time_id' in request.GET.dict():
                print(type(request.GET.get('date')))
                print(datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d"))
                cnv_dt = datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d")
                discipline_id = (TTLesson.objects
                                 .filter(date=cnv_dt,
                                         lesson_time_id=request.GET.get('lesson_time_id'),
                                         classroom_id=request.GET.get('classroom_id'))
                                 .values('curriculum_lesson_id__curriculum_id__discipline_id')
                                 .first())['curriculum_lesson_id__curriculum_id__discipline_id']
                print(discipline_id)
                # curriculum_lesson_objects = (CurriculumLesson.objects
                #                              .filter(curriculum_id__discipline_id=discipline_id)
                #                              .order_by('-curriculum_id__group_semester_id__semester_num',
                #                                        'lesson_type'))
                #
                # print(curriculum_lesson_objects)

                curriculum_lesson_objects = (CurriculumLesson.objects
                                             .filter(tutor_id__user_id__id__in=tutor_ids,
                                                     curriculum_id__discipline_id=discipline_id)
                                             .order_by('-curriculum_id__discipline_id__name',
                                                       'curriculum_id__group_semester_id__group_id__name',
                                                       '-curriculum_id__group_semester_id__semester_num',
                                                       'lesson_type'))
            # tt_lesson_form = TTLessonRegisterForm()
            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())


        elif 'classroom_id' in request.GET.dict() and 'group_ids' in request.GET.dict():
            print(request.GET.get('group_ids'))
            group_ids = literal_eval(request.GET.get('group_ids'))
            classroom_obj = get_object_or_404(Classroom, classroom_id=request.GET.get('classroom_id'))
            initial['classroom_id'] = classroom_obj
            tt_lesson_form = TTLessonRegisterForm(initial=initial)

            if 'date' in request.GET.dict() and 'lesson_time_id' in request.GET.dict():
                print(type(request.GET.get('date')))
                print(datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d"))
                cnv_dt = datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d")
                discipline_id = (TTLesson.objects
                                 .filter(date=cnv_dt,
                                         lesson_time_id=request.GET.get('lesson_time_id'),
                                         classroom_id=request.GET.get('classroom_id'))
                                 .values('curriculum_lesson_id__curriculum_id__discipline_id')
                                 .first())['curriculum_lesson_id__curriculum_id__discipline_id']
                print(discipline_id)
                # curriculum_lesson_objects = (CurriculumLesson.objects
                #                              .filter(curriculum_id__discipline_id=discipline_id)
                #                              .order_by('-curriculum_id__group_semester_id__semester_num',
                #                                        'lesson_type'))
                #
                # print(curriculum_lesson_objects)

                curriculum_lesson_objects = (CurriculumLesson.objects
                                             .filter(curriculum_id__group_semester_id__group_id__in=group_ids,
                                                     curriculum_id__discipline_id=discipline_id)
                                             .order_by('-curriculum_id__discipline_id__name',
                                                       'curriculum_id__group_semester_id__group_id__name',
                                                       '-curriculum_id__group_semester_id__semester_num',
                                                       'lesson_type'))
            # tt_lesson_form = TTLessonRegisterForm()
            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())


        elif 'classroom_id' in request.GET.dict():
            classroom_obj = get_object_or_404(Classroom, classroom_id=request.GET.get('classroom_id'))
            initial['classroom_id'] = classroom_obj
            tt_lesson_form = TTLessonRegisterForm(initial=initial)

            if 'date' in request.GET.dict() and 'lesson_time_id' in request.GET.dict():
                print(type(request.GET.get('date')))
                print(datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d"))
                cnv_dt = datetime.strptime(request.GET.get('date'), "%d.%m.%Y").strftime("%Y-%m-%d")
                discipline_id = (TTLesson.objects
                                 .filter(date=cnv_dt,
                                         lesson_time_id=request.GET.get('lesson_time_id'),
                                         classroom_id=request.GET.get('classroom_id'))
                                 .values('curriculum_lesson_id__curriculum_id__discipline_id')
                                 .first())['curriculum_lesson_id__curriculum_id__discipline_id']
                print(discipline_id)
                curriculum_lesson_objects = (CurriculumLesson.objects
                                             .filter(curriculum_id__discipline_id=discipline_id)
                                             .order_by('-curriculum_id__group_semester_id__semester_num',
                                                       'lesson_type'))

                print(curriculum_lesson_objects)

            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())

            # tt_lesson_form = TTLessonRegisterForm(initial={'classroom_id': classroom_obj})

        elif 'tutor_id' in request.GET.dict():
            curriculum_lesson_objects = (CurriculumLesson.objects
                                         .filter(tutor_id=request.GET.get('tutor_id'))
                                         .order_by('-curriculum_id__discipline_id__name',
                                                   'curriculum_id__group_semester_id__group_id__name',
                                                   '-curriculum_id__group_semester_id__semester_num',
                                                   'lesson_type'))
            # tt_lesson_form = TTLessonRegisterForm()
            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())
        elif 'student_id' in request.GET.dict():
            group_semester_ids = (GroupMember.objects
                                  .filter(student_id=request.GET.get('student_id'))
                                  .values('group_semester_id').all())

            curriculum_lesson_objects = (CurriculumLesson.objects
                                         .filter(curriculum_id__group_semester_id__in=group_semester_ids)
                                         .order_by('curriculum_id__group_semester_id__group_id__name',
                                                   '-curriculum_id__group_semester_id__semester_num'))
            # tt_lesson_form = TTLessonRegisterForm()
            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())
        elif 'group_id' in request.GET.dict():
            curriculum_lesson_objects = (CurriculumLesson.objects
                                         .filter(curriculum_id__group_semester_id__group_id=request.GET.get('group_id'))
                                         .order_by('-curriculum_id__group_semester_id__semester_num'))
            # tt_lesson_form = TTLessonRegisterForm()
            if curriculum_lesson_objects is not None:
                tt_lesson_form.set_initial_curriculum_lesson_ids(curriculum_lesson_objects.all())
        # else:
        #     tt_lesson_form = TTLessonRegisterForm()
    context = {'tt_lesson_form': tt_lesson_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'tt_lesson/tt_lesson_form.html', context=context)


@permission_required('timetable.change_ttlesson', raise_exception=True)
def tt_lesson_edit(request, tt_lesson_id):
    """
    View for editing timetable lesson information.
    :param request: user's request
    :param tt_lesson_id: timetable lesson entity identifier
    :return: HTTP response HTML page with form to edit timetable lesson information or redirect page
    """
    tt_lesson_obj = get_object_or_404(TTLesson, tt_lesson_id=tt_lesson_id)
    tt_lesson_obj.date = tt_lesson_obj.date.strftime("%d.%m.%Y")
    tt_lesson_form = TTLessonRegisterForm(request.POST or None, instance=tt_lesson_obj)
    if tt_lesson_form.is_valid():
        tt_lesson_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'занятие в расписании'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next').split('?')[0])
            return redirect(request.GET.get('next').replace(':', '&'))
        except Resolver404 or KeyError:
            return redirect(reverse('group:group_list'))
    context = {'tt_lesson_form': tt_lesson_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'tt_lesson/tt_lesson_form.html', context=context)


@permission_required('timetable.delete_ttlesson', raise_exception=True)
def tt_lesson_delete(request, tt_lesson_id):
    """
    View for deleting timetable lesson information.
    :param request: user's request
    :param tt_lesson_id: timetable lesson entity identifier
    :return: HTTP response HTML page with form to delete timetable lesson information or redirect page
    """
    tt_lesson_obj = get_object_or_404(TTLesson, tt_lesson_id=tt_lesson_id)
    if request.method == 'POST':
        request.session["obj_name"] = 'занятие в расписании'
        request.session["obj_action"] = 'D'
        try:
            print("%%%%%%")
            print(tt_lesson_obj)
            tt_lesson_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next').split('?')[0])
                return redirect(request.GET.get('next').replace(':', '&'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('group:group_list'))
        except Http404:
            return redirect(reverse('group:group_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next').split('?')[0])
                return redirect(request.GET.get('next').replace(':', '&'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('group:group_list'))
    context = {'tt_lesson': tt_lesson_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'tt_lesson/tt_lesson_delete.html', context=context)
