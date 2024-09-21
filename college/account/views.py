"""
Views for account app.
"""
from datetime import datetime, timedelta

import django.db.transaction
from django import forms
# import simplejson
from itertools import groupby
from django.urls import reverse, resolve, Resolver404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction, IntegrityError
from django.db.models import Max, ProtectedError, Subquery, OuterRef, Prefetch, Q
from django.db.models.expressions import Col, F
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Coalesce
from django.views.generic import UpdateView
from django.db import connection
from django.contrib.postgres.aggregates import StringAgg
from psycopg2.errors import UniqueViolation

from .forms import LoginForm, UserRegistrationForm, UserEditForm, StudentAdditionalForm, TutorAdditionalForm, \
    GroupRegisterForm, \
    DisciplineRegisterForm, ClassroomRegisterForm, LessonTimeRegisterForm, GroupSemesterRegisterForm, \
    GroupMemberRegisterForm, CurriculumRegisterForm, CurriculumLessonRegisterForm, TTLessonRegisterForm
from timetable.models import GroupSemester, Curriculum, Discipline, Tutor, LessonTime, Classroom, Student, CustomUser, \
    GroupMember, CurriculumLesson, Group, TypesOfLesson, TTLesson


def user_login(request):
    """
    View for logging user in.
    :param request: user's request
    :return: HTTP response HTML page with login form
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                return HttpResponse('Disabled account')
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    View for plug page.
    :param request: user's request
    :return: HTTP response plug HTML page
    """
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def user_list(request):
    """
    View for list of users.
    :param request: user's request
    :return: HTTP response HTML page with users list
    """
    users_list = (CustomUser.objects
                  .filter(is_superuser=False, is_staff=False, is_active=True)
                  .order_by('last_name', 'first_name', 'second_name')
                  .all())
    # print(request.user)
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context = {'users': users}
    context.update(obj_stats)
    return render(request, 'account/user_list.html', context=context)


def user_details(request, id):
    """
    View for user details.
    :param request: user's request
    :param id: user identifier
    :return: HTTP response HTML page with user details
    """
    print(request.user)
    user = get_object_or_404(CustomUser.objects, id=id)
    student = Student.objects.filter(user_id__id=id).first()
    tutor = Tutor.objects.filter(user_id__id=id).first()

    groups = GroupMember.objects.select_related('student_id__user_id',
                                                'group_semester_id__group_id') \
        .values('group_semester_id__group_id__name',
                'group_semester_id__semester_num',
                'group_semester_id__group_id__group_id') \
        .filter(student_id__user_id__id=id) \
        .all()

    disciplines = CurriculumLesson.objects.select_related('tutor_id__user_id',
                                                          'curriculum_id__discipline_id') \
        .values('curriculum_id__discipline_id__name',
                'curriculum_id__discipline_id__discipline_id') \
        .filter(tutor_id__user_id__id=id) \
        .all()
    # print(groups.query)

    context = {'user': user,
               'student': student,
               'tutor': tutor,
               'groups': groups,
               'disciplines': disciplines}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]

    context.update(obj_stats)
    context.update(tt_lesson_details(request))
    print(context)
    return render(request, 'account/user_detail.html', context=context)


@transaction.atomic
def user_register(request):
    """
    View for registering user.
    :param request: user's request
    :return: HTTP response HTML page with register form
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # student_form = StudentAdditionalForm(request.POST, prefix='std')
        # tutor_form = TutorAdditionalForm(False, request.POST, prefix='tut')
        # print(tutor_form.data)
        user_form.is_valid()
        print(user_form.is_valid())
        # print(user_form.cleaned_data['is_student'])
        # print(user_form.cleaned_data['is_tutor'])
        if user_form.cleaned_data['is_student']:
            # student_form.change_required(required=True)
            student_form = StudentAdditionalForm(True, request.POST, prefix='std')
            print("S-T")
        else:
            student_form = StudentAdditionalForm(False, request.POST, prefix='std')
            # student_form.change_required(required=False)
            print("S-F")
        if user_form.cleaned_data['is_tutor']:
            tutor_form = TutorAdditionalForm(True, request.POST, prefix='tut')
            # tutor_form.change_required(required=True)
            print("T-T")
        else:
            # tutor_form.change_required(required=False)
            tutor_form = TutorAdditionalForm(False, request.POST, prefix='tut')
            print("T-F")
        # student_form = StudentAdditionalForm(request.POST, prefix='std')
        # tutor_form = TutorAdditionalForm(True, request.POST, prefix='tut')
        # user_form.is_valid()
        if user_form.is_valid() and \
                ((user_form.cleaned_data['is_student'] and student_form.is_valid()) or not user_form.cleaned_data[
                    'is_student']) \
                and ((user_form.cleaned_data['is_tutor'] and tutor_form.is_valid()) or not user_form.cleaned_data[
            'is_tutor']):
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            if user_form.cleaned_data['is_student']:
                new_student = student_form.save(commit=False)
                new_student.set_user_id(new_user)
                new_student.save()
            if user_form.cleaned_data['is_tutor']:
                new_tutor = tutor_form.save(commit=False)
                new_tutor.set_user_id(new_user)
                new_tutor.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'пользователь'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:user_list'))
    else:
        user_form = UserRegistrationForm()
        student_form = StudentAdditionalForm(False, prefix='std')
        tutor_form = TutorAdditionalForm(False, prefix='tut')
    context = {'user_form': user_form,
               'student_form': student_form,
               'tutor_form': tutor_form,
               'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'account/user_register.html', context=context)


@transaction.atomic
def user_edit(request, id):
    """
    View for registering user.
    :param request: user's request
    :return: HTTP response HTML page with register form
    """
    # if request.method == 'POST':
    user_obj = get_object_or_404(CustomUser, id=id)
    student_obj = Student.objects.filter(user_id=user_obj.id).first()
    tutor_obj = Tutor.objects.filter(user_id=user_obj.id).first()
    user_form = UserEditForm(request.POST or None, instance=user_obj)
    if student_obj:
        student_obj.date_of_birth = student_obj.date_of_birth.strftime("%d.%m.%Y")
        student_form = StudentAdditionalForm(True, request.POST or None, instance=student_obj, prefix='std')
    else:
        student_form = StudentAdditionalForm(False, request.POST or None, instance=student_obj, prefix='std')
    if tutor_obj:
        tutor_obj.date_of_birth = tutor_obj.date_of_birth.strftime("%d.%m.%Y")
        tutor_form = TutorAdditionalForm(True, request.POST or None, instance=tutor_obj, prefix='tut')
    else:
        tutor_form = TutorAdditionalForm(False, request.POST or None, instance=tutor_obj, prefix='tut')

    # user_form = UserRegistrationForm(request.POST)
    # student_form = StudentAdditionalForm(request.POST, prefix='std')
    # tutor_form = TutorAdditionalForm(False, request.POST, prefix='tut')
    # print(tutor_form.data)
    # user_form.is_valid()
    print(user_form.is_valid())
    user_form.is_valid()
    print(student_form.data.getlist('std-date_of_birth', None))
    print(tutor_form.data.getlist('tut-date_of_birth', None))

    # print(user_form.cleaned_data['is_student'])
    # print(user_form.cleaned_data['is_tutor'])

    if True:
        if request.POST:
            std_date_of_birth = student_form.data.getlist('std-date_of_birth', None)[0]
            tut_date_of_birth = tutor_form.data.getlist('tut-date_of_birth', None)[0]
            if std_date_of_birth:
                # student_form.change_required(required=True)
                student_form = StudentAdditionalForm(True, request.POST or None, instance=student_obj, prefix='std')
                print("S-T")
            else:
                student_form = StudentAdditionalForm(False, request.POST or None, instance=student_obj,
                                                     prefix='std')
                # student_form.change_required(required=False)
                print("S-F")
            if tut_date_of_birth:
                tutor_form = TutorAdditionalForm(True, request.POST or None, instance=tutor_obj, prefix='tut')
                # tutor_form.change_required(required=True)
                print("T-T")
            else:
                # tutor_form.change_required(required=False)
                tutor_form = TutorAdditionalForm(False, request.POST or None, instance=tutor_obj, prefix='tut')
                print("T-F")
            # student_form = StudentAdditionalForm(request.POST, prefix='std')
            # tutor_form = TutorAdditionalForm(True, request.POST, prefix='tut')
            # user_form.is_valid()
            print(user_form.is_valid())
            print(std_date_of_birth and student_form.is_valid())
            print(not std_date_of_birth)
            print(tut_date_of_birth and tutor_form.is_valid())
            print(not tut_date_of_birth)
            print(user_form.errors)
            if user_form.is_valid() and \
                    ((std_date_of_birth and student_form.is_valid()) or not std_date_of_birth) \
                    and ((tut_date_of_birth and tutor_form.is_valid()) or not tut_date_of_birth):
                new_user = user_form.save(commit=False)
                new_user.save()
                print(std_date_of_birth)
                if std_date_of_birth:
                    print('std_date_of_birth')
                    new_student = student_form.save(commit=False)
                    new_student.set_user_id(user_obj)
                    new_student.save()
                print(tut_date_of_birth)
                if tut_date_of_birth:
                    print('tut_date_of_birth')
                    new_tutor = tutor_form.save(commit=False)
                    new_tutor.set_user_id(user_obj)
                    new_tutor.save()
                request.session["obj_status"] = 'success'
                request.session["obj_name"] = 'пользователь'
                request.session["obj_action"] = 'U'
                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('account:user_details', kwargs={'id': id}))
                # return render(request, 'account/register_done.html', {'new_user': new_user})
    # else:
    #     user_form = UserRegistrationForm()
    #     student_form = StudentAdditionalForm(False, prefix='std')
    #     tutor_form = TutorAdditionalForm(False, prefix='tut')
    # return render(request, 'account/user_register.html', {'user_form': user_form,
    #                                                          'student_form': student_form,
    #                                                          'tutor_form': tutor_form})

    context = {'user_form': user_form,
               'student_form': student_form,
               'tutor_form': tutor_form,
               'user': user_obj,
               'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'account/user_edit.html', context=context)


def user_delete(request, id):
    """
    View for deleting user information.
    :param request: user's request
    :param id: user identifier
    :return: HTTP response HTML page with form to delete user information or redirect page
    """
    user_obj = get_object_or_404(CustomUser, id=id)
    student_obj = Student.objects.filter(user_id=user_obj.id).first()
    tutor_obj = Tutor.objects.filter(user_id=user_obj.id).first()
    user = CustomUser.objects.get(id=id)

    if request.method == 'POST':
        request.session["obj_name"] = 'пользователь'
        request.session["obj_action"] = 'D'
        try:
            if student_obj:
                student_obj.delete()
            if tutor_obj:
                tutor_obj.delete()
            user_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                if resolve_match.url_name == 'user_details':
                    raise Http404
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_list'))
        except Http404:
            return redirect(reverse('account:user_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_details', kwargs={'id': id}))
    context = {'user': user}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'account/user_delete.html', context=context)


def user_delete_tutor(request, id):
    """
    View for deleting tutor information.
    :param request: user's request
    :param id: user identifier
    :return: HTTP response HTML page with form to delete tutor information or redirect page
    """
    tutor_obj = get_object_or_404(Tutor.objects, user_id__id=id)
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        request.session["obj_name"] = 'преподаватель'
        request.session["obj_action"] = 'D'
        try:
            tutor_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_details', kwargs={'id': id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_details', kwargs={'id': id}))
    context = {'user': user_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'account/tutor_delete.html', context=context)


def user_delete_student(request, id):
    """
    View for deleting student information.
    :param request: user's request
    :param id: user identifier
    :return: HTTP response HTML page with form to delete student information or redirect page
    """
    student_obj = get_object_or_404(Student.objects, user_id__id=id)
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        request.session["obj_name"] = 'студент'
        request.session["obj_action"] = 'D'
        try:
            student_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_details', kwargs={'id': id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:user_details', kwargs={'id': id}))
    context = {'user': user_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'account/tutor_delete.html', context=context)


# GROUP BLOCK


def group_list(request):
    """
    View for list of groups.
    :param request: user's request
    :return: HTTP response HTML page with groups list
    """
    groups = (Group.objects
              .annotate(max_sem=Coalesce(Subquery(GroupSemester.objects
                                                  .filter(group_id=OuterRef('group_id'))
                                                  .values('group_id')
                                                  .annotate(max_sem=Max('semester_num'))
                                                  .values('max_sem')
                                                  ), 0
                                         )
                        )
              .order_by('-max_sem', 'name')
              )
    print(groups.query)
    print(groups)
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context = {'groups': groups}
    context.update(obj_stats)
    return render(request, 'group/group_list.html', context=context)


def group_details(request, group_id):
    """
    View for group details.
    :param request: user's request
    :param group_id: group identifier
    :return: HTTP response HTML page with group details
    """
    group_obj = get_object_or_404(Group.objects, group_id=group_id)
    group_members_obj = (
        GroupMember.objects.select_related('group_semester_id__group_id',
                                           'student_id__user_id',
                                           'group_semester_id')
        .values(
            'group_semester_id__group_semester_id',
            'group_semester_id',
            'group_semester_id__semester_num',
            'group_member_id',
            'student_id__user_id__id',
            'student_id__user_id__last_name',
            'student_id__user_id__first_name',
            'student_id__user_id__second_name')
        .filter(group_semester_id__group_id__group_id=group_id)
        .order_by('-group_semester_id__semester_num',
                  'student_id__user_id__last_name',
                  'student_id__user_id__first_name',
                  'student_id__user_id__second_name')
        .all()
    )

    group_members_obj.query.alias_map['group_members'].join_type = "FULL OUTER JOIN"
    group_members_obj.query.alias_map['group_semesters'].join_type = "FULL OUTER JOIN"
    group_members_obj.query.alias_map['students'].join_type = "LEFT OUTER JOIN"
    group_members_obj.query.alias_map['timetable_customuser'].join_type = "LEFT OUTER JOIN"

    print(group_members_obj)
    print(group_members_obj.query)

    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM group_members gm \
    # 	FULL JOIN group_semesters gs ON gm.group_semester_id = gs.group_semester_id \
    # 	FULL JOIN students s ON gm.student_id = s.student_id \
    # WHERE gs.group_id = 5;")
    #         rows = cursor.fetchall()
    #     print(rows)

    # filter(Table2__field='value')

    group_lessons_obj = (CurriculumLesson.objects
                         .select_related('curriculum_id__discipline_id',
                                         'tutor_id__user_id',
                                         'curriculum_id__group_semester_id')
                         .values('curriculum_lesson_id',
                                 'lesson_type',
                                 'curriculum_id',
                                 'curriculum_id__discipline_id__name',
                                 'curriculum_id__discipline_id__discipline_id',
                                 'curriculum_id__group_semester_id__group_semester_id',
                                 'curriculum_id__group_semester_id__semester_num',
                                 'tutor_id__user_id__id',
                                 'tutor_id__user_id__last_name',
                                 'tutor_id__user_id__first_name',
                                 'tutor_id__user_id__second_name')
                         .filter(curriculum_id__group_semester_id__group_id__group_id=group_id)
                         .order_by('-curriculum_id__group_semester_id__semester_num',
                                   'curriculum_id__discipline_id__name',
                                   'tutor_id__user_id__last_name',
                                   'tutor_id__user_id__first_name',
                                   'tutor_id__user_id__second_name')
                         .all())

    # print(group_lessons_obj.query)
    # print(group_lessons_obj.query.alias_map.keys())

    group_lessons_obj.query.alias_map['curriculum_lessons'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['curriculums'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['disciplines'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['group_semesters'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['tutors'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['timetable_customuser'].join_type = "FULL OUTER JOIN"

    print(group_lessons_obj.query)
    print(group_lessons_obj)
    # groups_obj = (Curriculum.objects.select_related('group_semester_id__group_id')
    #               .values('group_semester_id__semester_num', 'group_semester_id__group_id__name',
    #                       'group_semester_id__group_id__group_id')
    #               .filter(discipline_id__discipline_id=discipline_id).all())
    # tutors_obj = (CurriculumLesson.objects.select_related('tutor_id__user_id')
    #               .values('tutor_id__user_id__id', 'tutor_id__user_id__last_name', 'tutor_id__user_id__first_name',
    #                       'tutor_id__user_id__second_name')
    #               .distinct()
    #               .filter(curriculum_id__discipline_id__discipline_id=discipline_id).all())

    # print(groups_obj.__dict__)

    context = {'group': group_obj,
               'group_members': group_members_obj,
               'group_lessons': group_lessons_obj,
               'lesson_types': dict(TypesOfLesson.choices)}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    # print(context)
    return render(request, 'group/group_detail.html', context=context)


@transaction.atomic
def group_register(request):
    """
    View for group registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register group or redirect page
    """
    if request.method == 'POST':
        group_form = GroupRegisterForm(request.POST)
        if group_form.is_valid():
            new_group = group_form.save(commit=False)
            new_group.save()
            new_group_semester = GroupSemester()
            new_group_semester.set_semester_num(1)
            new_group_semester.set_group_id(new_group)
            new_group_semester.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'группа'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:group_list'))
    else:
        group_form = GroupRegisterForm()
    context = {'group_form': group_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_form.html', context=context)


def group_edit(request, group_id):
    """
    View for editing group information.
    :param request: user's request
    :param group_id: group identifier
    :return: HTTP response HTML page with form to edit group information or redirect page
    """
    group_obj = get_object_or_404(Group, group_id=group_id)
    print(group_obj)
    group_form = GroupRegisterForm(request.POST or None, instance=group_obj)
    if group_form.is_valid():
        group_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'группа'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('account:group_details', kwargs={'group_id': group_id}))
    context = {'group_form': group_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_form.html', context=context)


def group_delete(request, group_id):
    """
    View for deleting group information.
    :param request: user's request
    :param group_id: group identifier
    :return: HTTP response HTML page with form to delete group information or redirect page
    """
    group_obj = get_object_or_404(Group, group_id=group_id)
    if request.method == 'POST':
        request.session["obj_name"] = 'группа'
        request.session["obj_action"] = 'D'
        try:
            group_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                if resolve_match.url_name == 'group_details':
                    raise Http404
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:group_list'))
        except Http404:
            return redirect(reverse('account:group_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:group_details', kwargs={'group_id': group_id}))
    context = {'group': group_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_delete.html', context=context)


# DISCIPLINE BLOCK


def discipline_list(request):
    """
    View for list of disciplines.
    :param request: user's request
    :return: HTTP response HTML page with disciplines list
    """
    disciplines_list = Discipline.objects.order_by('name').all()
    paginator = Paginator(disciplines_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        disciplines = paginator.page(page_number)
    except PageNotAnInteger:
        disciplines = paginator.page(1)
    except EmptyPage:
        disciplines = paginator.page(paginator.num_pages)
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context = {'disciplines': disciplines}
    context.update(obj_stats)
    return render(request, 'discipline/discipline_list.html', context=context)


def discipline_details(request, discipline_id):
    """
    View for discipline details.
    :param request: user's request
    :param discipline_id: discipline identifier
    :return: HTTP response HTML page with discipline details
    """
    discipline_obj = get_object_or_404(Discipline.objects, discipline_id=discipline_id)
    groups_obj = (Curriculum.objects.select_related('group_semester_id__group_id')
                  .values('group_semester_id__semester_num',
                          'group_semester_id__group_id__name',
                          'group_semester_id__group_id__group_id')
                  .filter(discipline_id__discipline_id=discipline_id)
                  .all())
    tutors_obj = (CurriculumLesson.objects.select_related('tutor_id__user_id')
                  .values('tutor_id__user_id__id',
                          'tutor_id__user_id__last_name',
                          'tutor_id__user_id__first_name',
                          'tutor_id__user_id__second_name')
                  .distinct()
                  .filter(curriculum_id__discipline_id__discipline_id=discipline_id)
                  .all())

    print(groups_obj.__dict__)

    context = {'discipline': discipline_obj,
               'groups': groups_obj,
               'tutors': tutors_obj}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    print(context)
    return render(request, 'discipline/discipline_detail.html', context=context)


def discipline_register(request):
    """
    View for discipline registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register discipline or redirect page
    """
    if request.method == 'POST':
        discipline_form = DisciplineRegisterForm(request.POST)
        if discipline_form.is_valid():
            new_discipline = discipline_form.save(commit=False)
            new_discipline.save()
            print(new_discipline)
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'дисциплина'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:discipline_list'))
    else:
        discipline_form = DisciplineRegisterForm()
    context = {'discipline_form': discipline_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_form.html', context=context)


def discipline_edit(request, discipline_id):
    """
    View for editing discipline information.
    :param request: user's request
    :param discipline_id: discipline identifier
    :return: HTTP response HTML page with form to edit discipline information or redirect page
    """
    discipline_obj = get_object_or_404(Discipline, discipline_id=discipline_id)
    print(discipline_obj)
    discipline_form = DisciplineRegisterForm(request.POST or None, instance=discipline_obj)
    if discipline_form.is_valid():
        discipline_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'дисциплина'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('account:discipline_details', kwargs={'discipline_id': discipline_id}))
    context = {'discipline_form': discipline_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_form.html', context=context)


def discipline_delete(request, discipline_id):
    """
    View for deleting discipline information.
    :param request: user's request
    :param discipline_id: discipline identifier
    :return: HTTP response HTML page with form to delete discipline information or redirect page
    """
    discipline_obj = get_object_or_404(Discipline, discipline_id=discipline_id)
    if request.method == 'POST':
        request.session["obj_name"] = 'дисциплина'
        request.session["obj_action"] = 'D'
        try:
            discipline_obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                if resolve_match.url_name == 'discipline_details':
                    raise Http404
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:discipline_list'))
        except Http404:
            return redirect(reverse('account:discipline_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('account:discipline_details', kwargs={'discipline_id': discipline_id}))
    context = {'discipline': discipline_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_delete.html', context=context)


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
    print(context)
    return render(request, 'classroom/classroom_detail.html', context=context)


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
                return redirect(reverse('account:classroom_list'))
    else:
        classroom_form = ClassroomRegisterForm()
    context = {'classroom_form': classroom_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_form.html', context=context)


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
            return redirect(reverse('account:classroom_details', kwargs={'classroom_id': classroom_id}))
    context = {'classroom_form': classroom_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_form.html', context=context)


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
                return redirect(reverse('account:classroom_list'))
        except Http404:
            return redirect(reverse('account:classroom_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:classroom_details', kwargs={'classroom_id': classroom_id}))
    context = {'classroom': classroom_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'classroom/classroom_delete.html', context=context)


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
    return render(request, 'lesson_time/lesson_time_list.html', context=context)


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
    return render(request, 'lesson_time/lesson_time_detail.html', context=context)


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
                return redirect(reverse('account:lesson_time_list'))
    else:
        lesson_time_form = LessonTimeRegisterForm()
    context = {'lesson_time_form': lesson_time_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_form.html', context=context)


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
            return redirect(reverse('account:lesson_time_details', kwargs={'lesson_id': lesson_id}))
    context = {'lesson_time_form': lesson_time_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_form.html', context=context)


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
                return redirect(reverse('account:lesson_time_list'))
        except Http404:
            return redirect(reverse('account:lesson_time_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:lesson_time_details', kwargs={'lesson_id': lesson_id}))
    context = {'lesson_time': lesson_time_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'lesson_time/lesson_time_delete.html', context=context)


# GROUP SEMESTER BLOCK


def load_max_semester(request):
    """
    View for resolving maximum semester number.
    :param request: user's request
    :return: JSON response with maximum semester number
    """
    group_id = request.GET.get('group_id', None)
    if group_id is not None:
        args = GroupSemester.objects.filter(group_id=group_id)
        max_sem_num = args.aggregate(Max('semester_num'))
        print(max_sem_num)
        return JsonResponse(max_sem_num)


def group_semester_register(request):
    """
    View for group semester registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register group semester entity or redirect page
    """
    group_obj = None
    if request.method == 'POST':
        group_semester_form = GroupSemesterRegisterForm(request.POST)
        if group_semester_form.is_valid():
            new_group_semester = group_semester_form.save(commit=False)
            new_group_semester.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'группа семестр'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:group_details',
                                        kwargs={'group_id': new_group_semester.group_id.group_id}))
    if 'group_id' in request.GET.dict():
        group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
        group_semester_form = GroupSemesterRegisterForm(initial={'group_id': group_obj})
    else:
        group_semester_form = GroupSemesterRegisterForm()
    context = {'group_semester_form': group_semester_form,
               'group': group_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group_semester/group_semester_register.html', context)


def group_semester_delete(request):
    """
    View for deleting group semester information.
    :param request: user's request
    :return: HTTP response HTML page with form to delete group semester information or redirect page
    """
    if 'group_id' and 'semester_num' in request.GET.dict():
        group_semester_obj = get_object_or_404(GroupSemester, group_id=request.GET.get('group_id'),
                                               semester_num=request.GET.get('semester_num'))
        group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
        if request.method == 'POST':
            request.session["obj_name"] = 'группа семестр'
            request.session["obj_action"] = 'D'
            try:
                group_semester_obj.delete()
                request.session["obj_status"] = 'success'

                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('account:group_details',
                                            kwargs={'group_id': group_obj.group_id}))
            except Http404:
                return redirect(reverse('account:group_details',
                                        kwargs={'group_id': group_obj.group_id}))
            except ProtectedError:
                request.session["obj_status"] = 'error'
                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('account:group_details',
                                            kwargs={'group_id': group_obj.group_id}))
        context = {'group_semester': group_semester_obj,
                   'group': group_obj}
        if 'next' in request.GET.keys():
            context['next_url'] = request.GET.get('next')
        return render(request, 'group_semester/group_semester_delete.html', context=context)


# GROUP MEMBER BLOCK


def group_member_register(request):
    """
    View for group member registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register group member entity or redirect page
    """
    obj = None
    if request.method == 'POST':
        group_member_form = GroupMemberRegisterForm(request.POST)
        if group_member_form.is_valid():
            new_group_member = group_member_form.save(commit=False)
            new_group_member.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'учащийся группы'
            request.session["obj_action"] = 'C'

            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:group_details',
                                        kwargs={'group_id': new_group_member.group_semester_id.group_id.group_id}))
    else:
        if 'student_id' in request.GET.dict():
            obj = get_object_or_404(Student, student_id=request.GET.get('student_id'))
            group_member_form = GroupMemberRegisterForm(initial={'student_id': obj})
        elif 'group_id' in request.GET.dict() and 'semester_num' in request.GET.dict():
            obj = get_object_or_404(GroupSemester, group_id=request.GET.get('group_id'),
                                    semester_num=request.GET.get('semester_num'))
            group_member_form = GroupMemberRegisterForm(initial={'group_semester_id': obj})
        elif 'group_id' in request.GET.dict():
            obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            objects = GroupSemester.objects.filter(group_id=request.GET.get('group_id')).order_by('-semester_num')
            if objects is not None:
                group_member_form = GroupMemberRegisterForm(initial={'group_semester_id': objects.first().pk})
            else:
                group_member_form = GroupMemberRegisterForm()
            group_member_form.set_initial_group_semester_ids(objects.all())
        else:
            group_member_form = GroupMemberRegisterForm()
    context = {'group_member_form': group_member_form,
               'group': obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group_member/group_member_register.html', context=context)


def group_member_delete(request, group_member_id):
    """
    View for deleting group member information.
    :param request: user's request
    :param group_member_id: group member entity identifier
    :return: HTTP response HTML page with form to delete group member information or redirect page
    """
    group_member_obj = get_object_or_404(
        GroupMember.objects.select_related('group_semester_id__group_id',
                                           'student_id__user_id')
        .values(
            'student_id__user_id__last_name',
            'student_id__user_id__first_name',
            'student_id__user_id__second_name',
            'group_semester_id__group_id__group_id',
            'group_semester_id__group_id__name',
            'group_semester_id__semester_num',
            'group_semester_id__group_id'),
        group_member_id=group_member_id)
    obj = GroupMember.objects.get(group_member_id=group_member_id)
    print(group_member_obj)
    if request.method == 'POST':
        request.session["obj_name"] = 'учащийся группы'
        request.session["obj_action"] = 'D'
        try:
            obj.delete()
            request.session["obj_status"] = 'success'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:group_details',
                                        kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
        except Http404:
            return redirect(reverse('account:group_details',
                                    kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:group_details',
                                        kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
    context = {'group_member': group_member_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group_member/group_member_delete.html', context=context)


# CURRICULUM BLOCK


@transaction.atomic
def curriculum_register(request):
    """
    View for curriculum registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register curriculum or redirect page
    """
    new_curriculum, group_obj = None, None
    if request.method == 'POST':

        curriculum_form = CurriculumRegisterForm(request.POST)

        if curriculum_form.is_valid():
            for group_semester_id in curriculum_form.data.getlist('group_semester_id', None):
                for discipline_id in curriculum_form.data.getlist('discipline_id', None):
                    # cobj = Curriculum.objects.filter(
                    #     discipline__discipline_id=discipline_id,
                    #     group_semester__group_semester_id=group_semester_id)
                    # print(cobj)
                    new_curriculum = Curriculum()
                    new_curriculum.set_discipline(Discipline.objects.get(discipline_id=discipline_id))
                    new_curriculum.set_group_semester(GroupSemester.objects.get(group_semester_id=group_semester_id))
                    new_curriculum.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'план занятий'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:curriculum_lesson_group_details',
                                        kwargs={'group_id': new_curriculum.group_semester_id.group_id.group_id}))

        else:
            err = curriculum_form.errors
            print(err)
            # else:
            # errors = curriculum_form.errors
            # return HttpResponse(simplejson.dumps(errors), status=422)
    else:
        if 'discipline_id' in request.GET.dict():
            group_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            curriculum_form = CurriculumRegisterForm(initial={'discipline_id': group_obj})
        elif 'group_id' in request.GET.dict() and 'semester_num' in request.GET.dict():
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            group_semester_obj = get_object_or_404(GroupSemester, group_id=request.GET.get('group_id'),
                                                   semester_num=request.GET.get('semester_num'))
            group_semesters_obj = (GroupSemester.objects
                                   .filter(group_id=request.GET.get('group_id')).order_by('-semester_num'))
            curriculum_form = CurriculumRegisterForm(initial={'group_semester_id': group_semester_obj})
            curriculum_form.set_initial_group_semester_ids(group_semesters_obj.all())
        elif 'group_id' in request.GET.dict():
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            group_semesters_obj = (GroupSemester.objects
                                   .filter(group_id=request.GET.get('group_id')).order_by('-semester_num'))
            curriculum_form = CurriculumRegisterForm(initial={'group_semester_id': group_semesters_obj.first()})
            curriculum_form.set_initial_group_semester_ids(group_semesters_obj.all())
        else:
            curriculum_form = CurriculumRegisterForm()
    context = {'curriculum_form': curriculum_form,
               'group': group_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum/curriculum_from.html', context)


def curriculum_delete(request):
    """
    View for deleting curriculum information.
    :param request: user's request
    :return: HTTP response HTML page with form to delete curriculum information or redirect page
    """
    if 'discipline_id' and 'group_semester_id' in request.GET.dict():
        curriculum_obj = get_object_or_404(Curriculum, discipline_id=request.GET.get('discipline_id'),
                                           group_semester_id=request.GET.get('group_semester_id'))
        group_semester_obj = get_object_or_404(
            GroupSemester.objects
            .select_related('group_id')
            .values('group_id',
                    'group_id__group_id',
                    'group_id__name',
                    'semester_num'),
            group_semester_id=request.GET.get('group_semester_id'))
        print(group_semester_obj.get('group_id__group_id'))
        discipline_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
        if request.method == 'POST':
            request.session["obj_name"] = 'план занятий'
            request.session["obj_action"] = 'D'
            try:
                curriculum_obj.delete()
                request.session["obj_status"] = 'success'

                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('account:curriculum_lesson_group_details',
                                            kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))
            except Http404:
                return redirect(reverse('account:curriculum_lesson_group_details',
                                        kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))
            except ProtectedError:
                request.session["obj_status"] = 'error'
                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('account:curriculum_lesson_group_details',
                                            kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))

        context = {'discipline': discipline_obj,
                   'group_semester': group_semester_obj}
        if 'next' in request.GET.keys():
            context['next_url'] = request.GET.get('next')
        return render(request, 'curriculum/curriculum_delete.html', context=context)


# CURRICULUM LESSON BLOCK


def curriculum_lesson_group_details(request, group_id):
    group_obj = get_object_or_404(Group, group_id=group_id)
    group_lessons_obj = (CurriculumLesson.objects
                         .select_related('curriculum_id__discipline_id',
                                         'tutor_id__user_id',
                                         'curriculum_id__group_semester_id')
                         .values('curriculum_lesson_id',
                                 'lesson_type',
                                 'duration',
                                 'curriculum_id',
                                 'curriculum_id__discipline_id__name',
                                 'curriculum_id__discipline_id__discipline_id',
                                 'curriculum_id__group_semester_id__group_semester_id',
                                 'curriculum_id__group_semester_id__semester_num',
                                 'tutor_id__user_id__id',
                                 'tutor_id__user_id__last_name',
                                 'tutor_id__user_id__first_name',
                                 'tutor_id__user_id__second_name')
                         .filter(curriculum_id__group_semester_id__group_id__group_id=group_id)
                         .order_by('-curriculum_id__group_semester_id__semester_num',
                                   'curriculum_id__discipline_id__name',
                                   'tutor_id__user_id__last_name',
                                   'tutor_id__user_id__first_name',
                                   'tutor_id__user_id__second_name')
                         .all())

    # print(group_lessons_obj.query)
    # print(group_lessons_obj.query.alias_map.keys())

    group_lessons_obj.query.alias_map['curriculum_lessons'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['curriculums'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['disciplines'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['group_semesters'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['tutors'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['timetable_customuser'].join_type = "FULL OUTER JOIN"

    print(group_lessons_obj.query)
    print(group_lessons_obj)
    # groups_obj = (Curriculum.objects.select_related('group_semester_id__group_id')
    #               .values('group_semester_id__semester_num', 'group_semester_id__group_id__name',
    #                       'group_semester_id__group_id__group_id')
    #               .filter(discipline_id__discipline_id=discipline_id).all())
    # tutors_obj = (CurriculumLesson.objects.select_related('tutor_id__user_id')
    #               .values('tutor_id__user_id__id', 'tutor_id__user_id__last_name', 'tutor_id__user_id__first_name',
    #                       'tutor_id__user_id__second_name')
    #               .distinct()
    #               .filter(curriculum_id__discipline_id__discipline_id=discipline_id).all())

    # print(groups_obj.__dict__)

    context = {'group': group_obj,
               'group_lessons': group_lessons_obj,
               'lesson_types': dict(TypesOfLesson.choices)}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    # print(context)
    return render(request, 'curriculum_lesson/curriculum_lesson_group_detail.html', context=context)


def curriculum_lesson_register(request):
    discipline_obj, group_obj, tutor_obj = None, None, None
    if request.method == 'POST':
        curriculum_lesson_form = CurriculumLessonRegisterForm(request.POST)
        if curriculum_lesson_form.is_valid():
            new_curriculum_lesson = curriculum_lesson_form.save(commit=False)
            new_curriculum_lesson.save()
            request.session["obj_status"] = 'success'
            request.session["obj_name"] = 'занятие из плана'
            request.session["obj_action"] = 'C'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': new_curriculum_lesson.curriculum_id.group_semester_id.group_id.group_id}))
    else:
        if 'group_id' in request.GET.dict() and 'group_semester_id' in request.GET.dict() and 'discipline_id' in request.GET.dict():
            # group_semester_obj = get_object_or_404(
            #     GroupSemester.objects.select_related('group_id').values('group_id', 'group_id__name', 'semester_num'),
            #     group_id=request.GET.get('group_id'),
            #     group_semester_id=request.GET.get('group_semester_id'))
            # print(group_semester_obj)
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            curriculum_obj = get_object_or_404(Curriculum, group_semester_id=request.GET.get('group_semester_id'),
                                               discipline_id=request.GET.get('discipline_id'))
            discipline_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))

            curriculum_lesson_form = CurriculumLessonRegisterForm(initial={'curriculum_id': curriculum_obj})
        elif 'tutor_id' in request.GET.dict():
            tutor_obj = get_object_or_404(Tutor, tutor_id=request.GET.get('tutor_id'))
            curriculum_lesson_form = CurriculumLessonRegisterForm(initial={'tutor_id': tutor_obj})
        elif 'discipline_id' in request.GET.dict():
            discipline_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            curriculums_obj = Curriculum.objects.filter(discipline_id=request.GET.get('discipline_id')).all()
            curriculum_lesson_form = CurriculumLessonRegisterForm()
            curriculum_lesson_form.set_initial_curriculum_ids(curriculums_obj)
        elif 'group_id' in request.GET.dict():
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            curriculums_obj = (Curriculum.objects
                               .select_related('group_semester_id')
                               .filter(group_semester_id__group_id=request.GET.get('group_id')).all())
            curriculum_lesson_form = CurriculumLessonRegisterForm()
            curriculum_lesson_form.set_initial_curriculum_ids(curriculums_obj)
        else:
            curriculum_lesson_form = CurriculumLessonRegisterForm()

    context = {'curriculum_lesson_form': curriculum_lesson_form,
               'discipline': discipline_obj,
               'group': group_obj,
               'tutor': tutor_obj,
               'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_form.html', context=context)


def curriculum_lesson_edit(request, curriculum_lesson_id):
    curriculum_lesson_obj = get_object_or_404(CurriculumLesson, curriculum_lesson_id=curriculum_lesson_id)
    # curriculum_lesson = (CurriculumLesson.objects
    #                      .select_related('curriculum_id__discipline_id',
    #                                      'curriculum_id__discipline_id__group_semester_id__group_id',
    #                                      'tutor_id__user_id')
    #                      .values('curriculum_id__discipline_id',
    #                              'curriculum_id__discipline_id__name',
    #                              'curriculum_id__group_semester_id',
    #                              'curriculum_id__group_semester_id__group_id',
    #                              'curriculum_id__group_semester_id__semester_num',
    #                              'curriculum_id__group_semester_id__group_id__name',
    #                              'tutor_id__user_id__last_name',
    #                              'tutor_id__user_id__first_name',
    #                              'tutor_id__user_id__second_name').get(curriculum_lesson_id=curriculum_lesson_id))
    curriculum_lesson_form = CurriculumLessonRegisterForm(request.POST or None, instance=curriculum_lesson_obj)
    if curriculum_lesson_form.is_valid():
        curriculum_lesson_form.save()
        request.session["obj_status"] = 'success'
        request.session["obj_name"] = 'занятие из плана'
        request.session["obj_action"] = 'U'
        try:
            resolve_match = resolve(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        except Resolver404 or KeyError:
            return redirect(reverse('account:curriculum_lesson_group_details',
                                    kwargs={
                                        'group_id': curriculum_lesson_obj.curriculum_id.group_semester_id.group_id.group_id}))

    context = {'curriculum_lesson_form': curriculum_lesson_form,
               'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_form.html', context=context)


def curriculum_lesson_delete(request, curriculum_lesson_id):
    curriculum_lesson_obj = get_object_or_404(CurriculumLesson, curriculum_lesson_id=curriculum_lesson_id)
    curriculum_lesson = (CurriculumLesson.objects
                         .select_related('curriculum_id__discipline_id',
                                         'curriculum_id__discipline_id__group_semester_id__group_id',
                                         'tutor_id__user_id')
                         .values('curriculum_id__discipline_id',
                                 'curriculum_id__discipline_id__name',
                                 'curriculum_id__group_semester_id',
                                 'curriculum_id__group_semester_id__group_id',
                                 'curriculum_id__group_semester_id__group_id__group_id',
                                 'curriculum_id__group_semester_id__semester_num',
                                 'curriculum_id__group_semester_id__group_id__name',
                                 'tutor_id__user_id__last_name',
                                 'tutor_id__user_id__first_name',
                                 'tutor_id__user_id__second_name').get(curriculum_lesson_id=curriculum_lesson_id))
    if request.method == 'POST':
        request.session["obj_name"] = 'занятие из плана'
        request.session["obj_action"] = 'D'
        try:
            curriculum_lesson_obj.delete()
            request.session["obj_status"] = 'success'

            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': curriculum_lesson.get(
                                                'curriculum_id__group_semester_id__group_id__group_id')}))
        except Http404:
            return redirect(reverse('account:curriculum_lesson_group_details',
                                    kwargs={
                                        'group_id': curriculum_lesson.get(
                                            'curriculum_id__group_semester_id__group_id__group_id')}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('account:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': curriculum_lesson.get(
                                                'curriculum_id__group_semester_id__group_id__group_id')}))
    context = {'curriculum_lesson': curriculum_lesson}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_delete.html', context=context)


# TT_LESSON BLOCK


def tt_lesson_details(request, user_id=None, classroom_id=None, group_id=None):
    context = None
    tt_lesson_objs = []
    if 'date' in request.GET.keys():
        start_dt = datetime.strptime(request.GET.get('date'), '%d.%m.%Y').date()
        day_count = 1
        # Case for classroom
    elif 'start_date' in request.GET.keys() and 'end_date' in request.GET.keys():
        start_dt = datetime.strptime(request.GET.get('start_date'), '%d.%m.%Y').date()
        end_dt = datetime.strptime(request.GET.get('end_date'), '%d.%m.%Y').date()
        day_count = (end_dt - start_dt).days + 1
    else:
        raise Http404

    for dt in [d for d in (start_dt + timedelta(n) for n in range(day_count))]:
        if classroom_id in request.GET.keys():
            obj = TTLesson.objects.filter(date=dt, classroom_id=request.GET.get('classroom_id'))
        # Case for group
        elif 'group_id' in request.GET.keys():
            # Searching for tt_lesson's identifiers (day_name, week_type, lessons_time_id) to get whole info about
            # all groups, tutors, etc. involved in the lesson
            tt_lessons = (TTLesson.objects
                          .select_related('curriculum_lesson_id__curriculum_id__group_semester_id__group_id')
                          .filter(date=dt,
                                  curriculum_lesson_id__curriculum_id__group_semester_id__group_id=
                                  request.GET.get('group_id'))
                          .values('day_name', 'week_type', 'curriculum_lesson_id', 'lessons_time_id'))

            day_name_list = [tt_lesson_id['day_name'] for tt_lesson_id in tt_lessons]
            week_type_list = [tt_lesson_id['week_type'] for tt_lesson_id in tt_lessons]
            lessons_time_id_list = [tt_lesson_id['lessons_time_id'] for tt_lesson_id in tt_lessons]
            obj = TTLesson.objects.filter(date=dt,
                                          day_name__in=day_name_list,
                                          week_type__in=week_type_list,
                                          lessons_time_id__in=lessons_time_id_list)
        # Case for users (tutors & students)
        elif 'user_id' in request.GET.keys():
            # Searching for tt_lesson's identifiers (day_name, week_type, lessons_time_id) related to tutor
            # to get whole info about all groups, tutors, etc. involved in the lesson
            tt_lesson_tutor = \
                (TTLesson.objects
                 .select_related('curriculum_lesson_id__tutor_id__user_id')
                 .filter(date=dt,
                         curriculum_lesson_id__tutor_id__user_id=request.GET.get('user_id'))
                 .values('day_name', 'week_type', 'curriculum_lesson_id', 'lessons_time_id'))

            # Getting info about all student's group_semester_ids (about student's group history (group + semester num))
            group_semester_ids = (GroupMember.objects.select_related('student_id__user_id')
                                  .filter(student_id__user_id=request.GET.get('user_id'))
                                  .values('group_semester_id')
                                  .all())
            # Searching for tt_lesson's identifiers (day_name, week_type, lessons_time_id) related to student
            # to get whole info about all groups, tutors, etc. involved in the lesson
            tt_lesson_student = \
                (TTLesson.objects
                 .select_related('curriculum_lesson_id__curriculum_id')
                 .filter(date=dt,
                         curriculum_lesson_id__curriculum_id__group_semester_id__in=group_semester_ids)
                 .values('day_name', 'week_type', 'curriculum_lesson_id', 'lessons_time_id'))

            tt_lesson_ids = tt_lesson_tutor.union(tt_lesson_student)
            day_name_list = [tt_lesson_id['day_name'] for tt_lesson_id in tt_lesson_ids]
            week_type_list = [tt_lesson_id['week_type'] for tt_lesson_id in tt_lesson_ids]
            lessons_time_id_list = [tt_lesson_id['lessons_time_id'] for tt_lesson_id in tt_lesson_ids]
            obj = (TTLesson.objects
                   .filter(date=dt,
                           day_name__in=day_name_list,
                           week_type__in=week_type_list,
                           lessons_time_id__in=lessons_time_id_list)
                   .order_by('date', 'lessons_time_id__start_time'))
        else:
            raise Http404

        # Grouping tt_lesson_objects by curriculum_lesson
        tt_lesson_obj = [
            {
                'date': list(key)[0],
                'day_name': list(key)[1],
                'week_type': list(key)[2],
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
                                'id': item.curriculum_lesson_id.tutor_id.user_id.id,
                                'last_name': item.curriculum_lesson_id.tutor_id.user_id.last_name,
                                'first_name': item.curriculum_lesson_id.tutor_id.user_id.first_name,
                                'second_name': item.curriculum_lesson_id.tutor_id.user_id.second_name
                            },
                        'group':
                            {
                                'group_id': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.group_id,
                                'name': item.curriculum_lesson_id.curriculum_id.group_semester_id.group_id.name
                            }
                    } for item in grp
                ]
            } for key, grp in
            groupby(obj, key=lambda x: (x.date,
                                        x.day_name,
                                        x.week_type,
                                        x.lessons_time_id,
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

    context = {'tt_lessons': tt_lesson_obj,
               'lesson_types': dict(TypesOfLesson.choices),
               'week_types': dict(TTLesson.TYPE_OF_WEEK_CHOICES),
               'day_names': dict(TTLesson.DAY_OF_WEEK_CHOICES)}
    return context
    return render(request, 'tt_lesson/tt_lesson_detail.html', context=context)


def tt_lesson_register(request):
    if request.method == 'POST':
        tt_lesson_form = TTLessonRegisterForm(request.POST)
        if tt_lesson_form.is_valid():
            new_tt_lesson = tt_lesson_form.save(commit=False)
            new_tt_lesson.set_day_name(tt_lesson_form.cleaned_data['date'])
            new_tt_lesson.set_week_type(tt_lesson_form.cleaned_data['date'])
            try:
                new_tt_lesson.save()
                return render(request, 'tt_lesson/tt_lesson_register_done.html', {'tt_lesson_form': new_tt_lesson})
            except IntegrityError as ex:
                if isinstance(ex.__cause__, UniqueViolation):
                    if ex.__cause__.diag.constraint_name == 'tt_lesson_day_week_time_curriculum_les_unique':
                        tt_lesson_form.add_error(None, "У группы уже есть занятие в это время")
                else:
                    tt_lesson_form.add_error(None, ex.__cause__)
    else:
        tt_lesson_form = TTLessonRegisterForm()
    return render(request, 'tt_lesson/tt_lesson_register.html', {'tt_lesson_form': tt_lesson_form})
