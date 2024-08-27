"""
Views for account app.
"""
import django.db.transaction
# import simplejson
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView

from .forms import LoginForm, UserRegistrationForm, StudentAdditionalForm, TutorAdditionalForm, GroupRegisterForm, \
    DisciplineRegisterForm, ClassroomRegisterForm, LessonTimeRegisterForm, GroupSemesterRegisterForm, \
    GroupMemberRegisterForm, CurriculumRegisterForm, CurriculumLessonRegisterForm, TTLessonRegisterForm
from timetable.models import GroupSemester, Curriculum, Discipline, Tutor, LessonTime


def user_login(request):
    """
    View for logging user in.
    :param request: user's request
    :return: http response HTML page with login form
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
    :return: http response plug HTML page
    """
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    """
    View for registering user.
    :param request: user's request
    :return: http response HTML page with register form
    """
    if request.method == 'POST':
        with (django.db.transaction.atomic()):
            user_form = UserRegistrationForm(request.POST)
            student_form = StudentAdditionalForm(request.POST, prefix='std')
            tutor_form = TutorAdditionalForm(request.POST, prefix='tut')
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
                return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        student_form = StudentAdditionalForm(prefix='std')
        tutor_form = TutorAdditionalForm(prefix='tut')
    return render(request, 'account/register.html', {'user_form': user_form,
                                                     'student_form': student_form,
                                                     'tutor_form': tutor_form})


@transaction.atomic
def register_group(request):
    if request.method == 'POST':
        group_form = GroupRegisterForm(request.POST)
        if group_form.is_valid():
            new_group = group_form.save(commit=False)
            new_group.save()
            new_group_semester = GroupSemester()
            new_group_semester.set_semester_num(1)
            new_group_semester.set_group_id(new_group)
            new_group_semester.save()
            return render(request, 'group/group_register_done.html', {'group_form': group_form})

    else:
        group_form = GroupRegisterForm()
    return render(request, 'group/group_register.html', {'group_form': group_form})


def register_discipline(request):
    if request.method == 'POST':
        discipline_form = DisciplineRegisterForm(request.POST)
        if discipline_form.is_valid():
            new_discipline = discipline_form.save(commit=False)
            new_discipline.save()
            print(new_discipline)
            return render(request, 'discipline/discipline_register_done.html', {'discipline_form': discipline_form})

    else:
        discipline_form = DisciplineRegisterForm()
    return render(request, 'discipline/discipline_register.html', {'discipline_form': discipline_form})


def register_classroom(request):
    if request.method == 'POST':
        classroom_form = ClassroomRegisterForm(request.POST)
        if classroom_form.is_valid():
            new_classroom = classroom_form.save(commit=False)
            new_classroom.save()
            print(new_classroom)
            return render(request, 'classroom/classroom_register_done.html', {'classroom_form': classroom_form})

    else:
        classroom_form = ClassroomRegisterForm()
    return render(request, 'classroom/classroom_register.html', {'classroom_form': classroom_form})


def lesson_time_list(request):
    lesson_times = LessonTime.objects.all()
    return render(request, 'lesson_time/lesson_time_list.html', {'lesson_times': lesson_times})


def lesson_time_register(request):
    if request.method == 'POST':
        lesson_time_form = LessonTimeRegisterForm(request.POST)
        if lesson_time_form.is_valid():
            new_lesson_time = lesson_time_form.save(commit=False)
            new_lesson_time.save()
            print(new_lesson_time)
            return render(request, 'lesson_time/lesson_time_detail.html',
                          {'lesson_time': new_lesson_time,
                           'action': 'C'})
    else:
        lesson_time_form = LessonTimeRegisterForm()
    return render(request, 'lesson_time/lesson_time_form.html',
                  {'lesson_time_form': lesson_time_form,
                   'action': 'C'})


def lesson_time_details(request, lesson_id):
    context = {'lesson_time': LessonTime.objects.get(lesson_id=lesson_id)}
    print(context)
    return render(request, 'lesson_time/lesson_time_detail.html', context)


def lesson_time_edit(request, lesson_id):
    obj = get_object_or_404(LessonTime, lesson_id=lesson_id)
    lesson_time_form = LessonTimeRegisterForm(request.POST or None, instance=obj)
    if lesson_time_form.is_valid():
        lesson_time_form.save()
        print({'lesson_time': lesson_time_form,
               'action': 'E'})
        return render(request, 'lesson_time/lesson_time_detail.html',
                      {'lesson_time': obj,
                       'action': 'E'})
    return render(request, 'lesson_time/lesson_time_form.html',
                  {'lesson_time_form': lesson_time_form,
                   'action': 'E'})


def lesson_time_delete(request, lesson_id):
    obj = get_object_or_404(LessonTime, lesson_id=lesson_id)
    lesson_time = LessonTime.objects.get(lesson_id=lesson_id)
    if request.method == 'POST':
        obj.delete()
        return render(request, 'lesson_time/lesson_time_detail.html',
                      {'lesson_time': lesson_time,
                       'action': 'D'})
    return render(request, 'lesson_time/lesson_time_delete.html', {'lesson_time': lesson_time})


def load_max_semester(request):
    group_id = request.GET.get('group_id', None)
    if group_id is not None:
        args = GroupSemester.objects.filter(group_id=group_id)
        max_sem_num = args.aggregate(Max('semester_num'))
        print(max_sem_num)
        return JsonResponse(max_sem_num)


def register_group_semester(request):
    if request.method == 'POST':
        group_semester_form = GroupSemesterRegisterForm(request.POST)
        if group_semester_form.is_valid():
            new_group_semester = group_semester_form.save(commit=False)
            new_group_semester.save()
            return render(request, 'group_semester/group_semester_register_done.html',
                          {'group_semester_form': new_group_semester})
    else:
        group_semester_form = GroupSemesterRegisterForm()
    return render(request, 'group_semester/group_semester_register.html', {'group_semester_form': group_semester_form})


def register_group_member(request):
    if request.method == 'POST':
        group_member_form = GroupMemberRegisterForm(request.POST)
        if group_member_form.is_valid():
            new_group_member = group_member_form.save(commit=False)
            new_group_member.save()
            return render(request, 'group_member/group_member_register_done.html',
                          {'group_member_form': new_group_member})
    else:
        group_member_form = GroupMemberRegisterForm()
    return render(request, 'group_member/group_member_register.html', {'group_member_form': group_member_form})


@transaction.atomic
def register_curriculum(request):
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
            return render(request, 'curriculum/curriculum_register_done.html',
                          {'curriculum_form': new_curriculum})
        else:
            err = curriculum_form.errors
            print(err)
            # else:
            # errors = curriculum_form.errors
            # return HttpResponse(simplejson.dumps(errors), status=422)
    else:
        curriculum_form = CurriculumRegisterForm()
    return render(request, 'curriculum/curriculum_register.html', {'curriculum_form': curriculum_form})


def register_curriculum_lesson(request):
    if request.method == 'POST':
        curriculum_lesson_form = CurriculumLessonRegisterForm(request.POST)
        if curriculum_lesson_form.is_valid():
            new_curriculum_lesson = curriculum_lesson_form.save(commit=False)
            new_curriculum_lesson.save()
            return render(request, 'curriculum_lesson/curriculum_lesson_register_done.html',
                          {'curriculum_lesson_form': new_curriculum_lesson})
    else:
        curriculum_lesson_form = CurriculumLessonRegisterForm()
    return render(request, 'curriculum_lesson/curriculum_lesson_register.html',
                  {'curriculum_lesson_form': curriculum_lesson_form})


def register_tt_lesson(request):
    if request.method == 'POST':
        tt_lesson_form = TTLessonRegisterForm(request.POST)
        if tt_lesson_form.is_valid():
            new_tt_lesson = tt_lesson_form.save(commit=False)
            new_tt_lesson.save()
            return render(request, 'tt_lesson/tt_lesson_register_done.html',
                          {'tt_lesson_form': new_tt_lesson})
    else:
        tt_lesson_form = TTLessonRegisterForm()
    return render(request, 'tt_lesson/tt_lesson_register.html', {'tt_lesson_form': tt_lesson_form})
