"""
Views for curriculum app.
"""

from django.urls import reverse, resolve, Resolver404
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import DisciplineRegisterForm, CurriculumRegisterForm, CurriculumLessonRegisterForm

from user.models import Tutor
from group.models import Group, GroupSemester
from .models import Discipline, Curriculum, CurriculumLesson, TypesOfLesson


# DISCIPLINE BLOCK

@permission_required('curriculum.view_discipline', raise_exception=True)
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
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_list.html', context=context)


@permission_required('curriculum.view_discipline', raise_exception=True)
def discipline_details(request, discipline_id):
    """
    View for discipline details.
    :param request: user's request
    :param discipline_id: discipline identifier
    :return: HTTP response HTML page with discipline details
    """
    discipline_obj = get_object_or_404(Discipline.objects, discipline_id=discipline_id)
    groups_obj = (Curriculum.objects.select_related('group_semester_id__group_id')
                  .values('curriculum_id',
                          'group_semester_id',
                          'group_semester_id__semester_num',
                          'group_semester_id__group_id__name',
                          'group_semester_id__group_id__group_id')
                  .filter(discipline_id__discipline_id=discipline_id)
                  .order_by('-group_semester_id__semester_num',
                            'group_semester_id__group_id__name')
                  .all())
    tutors_obj = (CurriculumLesson.objects.select_related('tutor_id__user_id')
                  .values(
                          # 'curriculum_lesson_id',
                          'tutor_id__user_id__id',
                          'tutor_id__user_id__last_name',
                          'tutor_id__user_id__first_name',
                          'tutor_id__user_id__second_name')
                  .filter(curriculum_id__discipline_id__discipline_id=discipline_id)
                  .order_by('tutor_id__user_id__last_name',
                            'tutor_id__user_id__first_name',
                            'tutor_id__user_id__second_name')
                  .distinct()
                  .all())

    print(groups_obj.__dict__)
    print(tutors_obj.__dict__)

    context = {'discipline': discipline_obj,
               'groups': groups_obj,
               'tutors': tutors_obj}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    print(context)
    return render(request, 'discipline/discipline_details.html', context=context)


@permission_required('curriculum.register_discipline', raise_exception=True)
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
                return redirect(reverse('curriculum:discipline_list'))
    else:
        discipline_form = DisciplineRegisterForm()
    context = {'discipline_form': discipline_form, 'action': 'C'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_form.html', context=context)


@permission_required('curriculum.change_discipline', raise_exception=True)
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
            return redirect(reverse('curriculum:discipline_details', kwargs={'discipline_id': discipline_id}))
    context = {'discipline_form': discipline_form, 'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_form.html', context=context)


@permission_required('curriculum.delete_discipline', raise_exception=True)
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
                return redirect(reverse('curriculum:discipline_list'))
        except Http404:
            return redirect(reverse('curriculum:discipline_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('curriculum:discipline_details', kwargs={'discipline_id': discipline_id}))
    context = {'discipline': discipline_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'discipline/discipline_delete.html', context=context)


# CURRICULUM BLOCK

@permission_required('curriculum.add_curriculum', raise_exception=True)
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
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={'group_id': new_curriculum.group_semester_id.group_id.group_id}))

        else:
            err = curriculum_form.errors
            print(err)
            # else:
            # errors = curriculum_form.errors
            # return HttpResponse(simplejson.dumps(errors), status=422)
    else:
        if 'discipline_id' in request.GET.dict() and 'semester_num' in request.GET.dict():
            group_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            group_semesters_obj = (GroupSemester.objects
                                   .filter(semester_num=request.GET.get('semester_num'))
                                   .order_by('-semester_num', 'group_id__name'))
            curriculum_form = CurriculumRegisterForm(initial={'discipline_id': group_obj})
            curriculum_form.set_initial_group_semester_ids(group_semesters_obj.all())
        elif 'discipline_id' in request.GET.dict():
            group_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            curriculum_form = CurriculumRegisterForm(initial={'discipline_id': group_obj})
        elif 'group_id' in request.GET.dict() and 'semester_num' in request.GET.dict():
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            group_semester_obj = get_object_or_404(GroupSemester, group_id=request.GET.get('group_id'),
                                                   semester_num=request.GET.get('semester_num'))
            group_semesters_obj = (GroupSemester.objects
                                   .filter(group_id=request.GET.get('group_id'))
                                   .order_by('-semester_num', 'group_id__name'))
            curriculum_form = CurriculumRegisterForm(initial={'group_semester_id': group_semester_obj})
            curriculum_form.set_initial_group_semester_ids(group_semesters_obj.all())
        elif 'group_id' in request.GET.dict():
            group_obj = get_object_or_404(Group, group_id=request.GET.get('group_id'))
            group_semesters_obj = (GroupSemester.objects
                                   .filter(group_id=request.GET.get('group_id'))
                                   .order_by('-semester_num'))
            curriculum_form = CurriculumRegisterForm(initial={'group_semester_id': group_semesters_obj.first()})
            curriculum_form.set_initial_group_semester_ids(group_semesters_obj.all())
        else:
            curriculum_form = CurriculumRegisterForm()
    context = {'curriculum_form': curriculum_form,
               'group': group_obj}
    print(context)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum/curriculum_from.html', context)


@permission_required('curriculum.delete_curriculum', raise_exception=True)
def curriculum_delete(request, curriculum_id=None):
    """
    View for deleting curriculum information.
    :param curriculum_id: curriculum identifier
    :param request: user's request
    :return: HTTP response HTML page with form to delete curriculum information or redirect page
    """
    if 'discipline_id' and 'group_semester_id' in request.GET.dict():
        curriculum_obj = get_object_or_404(Curriculum, discipline_id=request.GET.get('discipline_id'),
                                           group_semester_id=request.GET.get('group_semester_id'))
        group_semester_id = request.GET.get('group_semester_id')
        discipline_id = request.GET.get('discipline_id')

    elif curriculum_id is not None:
        curriculum_obj = get_object_or_404(Curriculum, curriculum_id=curriculum_id)

        group_semester_id = curriculum_obj.group_semester_id.group_semester_id
        discipline_id = curriculum_obj.discipline_id.discipline_id

    else:
        raise Http404

    group_semester_obj = get_object_or_404(
        GroupSemester.objects
        .select_related('group_id')
        .values('group_id',
                'group_id__group_id',
                'group_id__name',
                'semester_num'),
        group_semester_id=group_semester_id)
    print(group_semester_obj.get('group_id__group_id'))
    discipline_obj = get_object_or_404(Discipline, discipline_id=discipline_id)

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
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))
        except Http404:
            return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                    kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={'group_id': group_semester_obj.get('group_id__group_id')}))

    context = {'discipline': discipline_obj,
               'group_semester': group_semester_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum/curriculum_delete.html', context=context)


# CURRICULUM LESSON BLOCK

@permission_required('curriculum.view_curriculumlesson', raise_exception=True)
def curriculum_lesson_group_details(request, group_id):
    # print(request.user.get_all_permissions())
    # print("000001")
    """
    View for curriculum lesson details.
    :param request: user's request
    :param group_id: group identifier
    :return: HTTP response HTML page with curriculum lesson details
    """
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
                                   'lesson_type',
                                   'tutor_id__user_id__last_name',
                                   'tutor_id__user_id__first_name',
                                   'tutor_id__user_id__second_name',
                                   'tutor_id__user_id__id')
                         .all())

    # print(group_lessons_obj.query)
    # print(group_lessons_obj.query.alias_map.keys())

    group_lessons_obj.query.alias_map['curriculum_lessons'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['curriculums'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['disciplines'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['group_semesters'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['tutors'].join_type = "FULL OUTER JOIN"
    group_lessons_obj.query.alias_map['user_customuser'].join_type = "FULL OUTER JOIN"

    if group_lessons_obj:
        max_semester = max([gm.get('curriculum_id__group_semester_id__semester_num') for gm in group_lessons_obj])
    else:
        max_semester = 0

    print(group_lessons_obj.query)
    print(group_lessons_obj)

    # print(groups_obj.__dict__)

    context = {'group': group_obj,
               'group_lessons': group_lessons_obj,
               'lesson_types': dict(TypesOfLesson.choices),
               'max_semester': max_semester}
    obj_stats = {key: value for key, value in request.session.items() if key.startswith('obj_')}
    if obj_stats:
        for obj_stat in obj_stats:
            del request.session[obj_stat]
    context.update(obj_stats)
    # print(context)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_group_details.html', context=context)


@permission_required('curriculum.add_curriculumlesson', raise_exception=True)
def curriculum_lesson_register(request):
    """
    View for curriculum lesson registration.
    :param request: user's request
    :return: HTTP response HTML page with form to register curriculum lesson or redirect page
    """
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
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': new_curriculum_lesson.curriculum_id.group_semester_id.group_id.group_id}))
    else:
        if 'group_id' in request.GET.dict() and 'group_semester_id' in request.GET.dict() and 'discipline_id' in request.GET.dict():
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


@permission_required('curriculum.change_curriculumlesson', raise_exception=True)
def curriculum_lesson_edit(request, curriculum_lesson_id):
    """
    View for editing curriculum lesson information.
    :param request: user's request
    :param curriculum_lesson_id: curriculum lesson entity identifier
    :return: HTTP response HTML page with form to edit curriculum lesson information or redirect page
    """
    curriculum_lesson_obj = get_object_or_404(CurriculumLesson, curriculum_lesson_id=curriculum_lesson_id)

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
            return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                    kwargs={
                                        'group_id': curriculum_lesson_obj.curriculum_id.group_semester_id.group_id.group_id}))

    context = {'curriculum_lesson_form': curriculum_lesson_form,
               'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_form.html', context=context)


@permission_required('curriculum.delete_curriculumlesson', raise_exception=True)
def curriculum_lesson_delete(request, curriculum_lesson_id):
    """
    View for deleting curriculum lesson information.
    :param request: user's request
    :param curriculum_lesson_id: curriculum lesson entity identifier
    :return: HTTP response HTML page with form to delete curriculum lesson information or redirect page
    """
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
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': curriculum_lesson.get(
                                                'curriculum_id__group_semester_id__group_id__group_id')}))
        except Http404:
            return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                    kwargs={
                                        'group_id': curriculum_lesson.get(
                                            'curriculum_id__group_semester_id__group_id__group_id')}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError:
                return redirect(reverse('curriculum:curriculum_lesson_group_details',
                                        kwargs={
                                            'group_id': curriculum_lesson.get(
                                                'curriculum_id__group_semester_id__group_id__group_id')}))
    context = {'curriculum_lesson': curriculum_lesson}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'curriculum_lesson/curriculum_lesson_delete.html', context=context)
