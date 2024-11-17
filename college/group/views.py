"""
Views for group app.
"""

from django.urls import reverse, resolve, Resolver404
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.db.models import Max, ProtectedError, Subquery, OuterRef
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Coalesce
from django.apps import apps

from .forms import GroupRegisterForm, GroupMemberRegisterForm, GroupSemesterRegisterForm
from timetable.models import TypesOfLesson
from timetable.views import tt_lesson_details


GroupSemester = apps.get_model('timetable', 'GroupSemester')
Student = apps.get_model('timetable', 'Student')
GroupMember = apps.get_model('timetable', 'GroupMember')
CurriculumLesson = apps.get_model('timetable', 'CurriculumLesson')
Group = apps.get_model('timetable', 'Group')


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
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
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
            'group_semester_id__group_id',
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
    max_semester = max([gm.get('group_semester_id__semester_num') for gm in group_members_obj])

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
               'lesson_types': dict(TypesOfLesson.choices),
               'max_semester': max_semester}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    context.update(tt_lesson_details(request, group_id=group_id))

    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    # print(context)
    return render(request, 'group/group_detail.html', context=context)


@permission_required('timetable.add_group', raise_exception=True)
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
                return redirect(reverse('group:group_list'))
    else:
        group_form = GroupRegisterForm()
    context = {'group_form': group_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_form.html', context=context)


@permission_required('timetable.change_group', raise_exception=True)
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
            return redirect(reverse('group:group_details', kwargs={'group_id': group_id}))
    context = {'group_form': group_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_form.html', context=context)


@permission_required('timetable.delete_group', raise_exception=True)
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
                return redirect(reverse('group:group_list'))
        except Http404:
            return redirect(reverse('group:group_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('group:group_details', kwargs={'group_id': group_id}))
    context = {'group': group_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group/group_delete.html', context=context)


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


@permission_required('timetable.add_groupsemester', raise_exception=True)
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
                return redirect(reverse('group:group_details',
                                        kwargs={'group_id': new_group_semester.group_id.group_id}))
    else:
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


@permission_required('timetable.delete_groupsemester', raise_exception=True)
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
                    return redirect(reverse('group:group_details',
                                            kwargs={'group_id': group_obj.group_id}))
            except Http404:
                return redirect(reverse('group:group_details',
                                        kwargs={'group_id': group_obj.group_id}))
            except ProtectedError:
                request.session["obj_status"] = 'error'
                try:
                    resolve_match = resolve(request.GET.get('next'))
                    return redirect(request.GET.get('next'))
                except Resolver404 or KeyError:
                    return redirect(reverse('group:group_details',
                                            kwargs={'group_id': group_obj.group_id}))
        context = {'group_semester': group_semester_obj,
                   'group': group_obj}
        if 'next' in request.GET.keys():
            context['next_url'] = request.GET.get('next')
        return render(request, 'group_semester/group_semester_delete.html', context=context)


# GROUP MEMBER BLOCK


@permission_required('timetable.add_groupmember', raise_exception=True)
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
                return redirect(reverse('group:group_details',
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


@permission_required('timetable.delete_groupmember', raise_exception=True)
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
                return redirect(reverse('group:group_details',
                                        kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
        except Http404:
            return redirect(reverse('group:group_details',
                                    kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('group:group_details',
                                        kwargs={'group_id': obj.group_semester_id.group_id.group_id}))
    context = {'group_member': group_member_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'group_member/group_member_delete.html', context=context)
