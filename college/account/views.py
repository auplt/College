"""
Views for account app.
"""
import django.db.transaction
from django import forms
# import simplejson
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max, ProtectedError, Subquery, OuterRef, Prefetch
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView

from .forms import LoginForm, UserRegistrationForm, UserEditForm, StudentAdditionalForm, TutorAdditionalForm, \
    GroupRegisterForm, \
    DisciplineRegisterForm, ClassroomRegisterForm, LessonTimeRegisterForm, GroupSemesterRegisterForm, \
    GroupMemberRegisterForm, CurriculumRegisterForm, CurriculumLessonRegisterForm, TTLessonRegisterForm
from timetable.models import GroupSemester, Curriculum, Discipline, Tutor, LessonTime, Classroom, Student, CustomUser, \
    GroupMember, CurriculumLesson


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


def user_list(request):
    users = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    # print(request.user)
    return render(request, 'account/user_list.html', {'users': users})


def user_details(request, id):
    print(request.user)
    user = get_object_or_404(CustomUser.objects, id=id)
    student = Student.objects.filter(user_id__id=id).first()
    tutor = Tutor.objects.filter(user_id__id=id).first()
    # users = CustomUser.objects.filter(id=id).annotate(student_id, date_of_birth_student=Subquery(subquery_student),
    #                                                 date_of_birth_tutor=Subquery(subquery_tutor))

    # users = CustomUser.objects.filter(id=id).prefetch_related(
    #     Prefetch('student_id',
    #                     queryset=subquery_student,
    #                     to_attr='student_records'
    #                     )
    #
    # ).prefetch_related(
    #     Prefetch('tutor_id',
    #                     queryset=subquery_tutor,
    #                     to_attr='tutor_records'
    #                     ))

    # groups =(GroupMember.objects
    #           .prefetch_related(
    #     Prefetch('student_id__user_id', queryset=CustomUser.objects.filter(id=id)))
    #           .prefetch_related('group_semesters'))
    # .select_related(
    #     'group_semesters')
    # groups = GroupMember.objects.prefetch_related(Prefetch('student_id',
    #     queryset=Student.objects.prefetch_related(Prefetch('user_id',
    #         queryset=CustomUser.objects.filter(id=id))),
    #     )).select_related('group_semesters__group_id')

    # groups = GroupMember.objects.prefetch_related(
    #     Prefetch('student_id__user_id', queryset=CustomUser.objects.filter(id=id)
    #
    #     )).select_related('group_semesters__group_id')

    # print(CustomUser.objects.filter(id=id))
    # print(groups.query)
    # print(groups)
    # print(groups.__dict__)
    # for group in groups:
    #
    #     print(group.__dict__)
    #     try:
    #         print(group.__dict__)
    #         print(group.student_id.__dict__)
    #         print(group.student_id.user_id.__dict__)
    #
    #         # print(group.student_id.test)
    #         # print(type(group.student_id.user_id.test))
    #     except Exception:
    #         pass
    # print(groups.get(student_id=5).student_id.user_id)
    # print(groups.get(student_id=5).group_semesters.group_id)
    # print(groups.filter(user_id=5).query)
    # GroupMember.objects.filter(student_id=)

    groups = GroupMember.objects.select_related('student_id__user_id', 'group_semesters__group_id') \
        .values('group_semesters__group_id__name', 'group_semesters__semester_num',
                'group_semesters__group_id__group_id') \
        .filter(student_id__user_id__id=id).all()

    disciplines = CurriculumLesson.objects.select_related('tutor_id__user_id', 'curriculum_id__discipline_id') \
        .values('curriculum_id__discipline_id__name', 'curriculum_id__discipline_id__discipline_id') \
        .filter(tutor_id__user_id__id=id).all()
    # print(groups.query)

    context = {'user': user, 'student': student, 'tutor': tutor, 'groups': groups, 'disciplines': disciplines}
    print(context)
    return render(request, 'account/user_detail.html', context)


def user_register(request):
    """
    View for registering user.
    :param request: user's request
    :return: http response HTML page with register form
    """
    if request.method == 'POST':
        with (django.db.transaction.atomic()):
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
                # return render(request, 'account/register_done.html', {'new_user': new_user})
                return render(request, 'account/user_result.html',
                              {'user': new_user,
                               'action': 'C'})
    else:
        user_form = UserRegistrationForm()
        student_form = StudentAdditionalForm(False, prefix='std')
        tutor_form = TutorAdditionalForm(False, prefix='tut')
    return render(request, 'account/user_register.html', {'user_form': user_form,
                                                          'student_form': student_form,
                                                          'tutor_form': tutor_form})


def user_edit(request, id):
    """
    View for registering user.
    :param request: user's request
    :return: http response HTML page with register form
    """
    # if request.method == 'POST':
    with (django.db.transaction.atomic()):
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
                    # return render(request, 'account/register_done.html', {'new_user': new_user})
                    return render(request, 'account/user_result.html',
                                  {'user': new_user,
                                   'action': 'E'})
    # else:
    #     user_form = UserRegistrationForm()
    #     student_form = StudentAdditionalForm(False, prefix='std')
    #     tutor_form = TutorAdditionalForm(False, prefix='tut')
    # return render(request, 'account/user_register.html', {'user_form': user_form,
    #                                                          'student_form': student_form,
    #                                                          'tutor_form': tutor_form})
    return render(request, 'account/user_edit.html',
                  {'user_form': user_form,
                   'student_form': student_form,
                   'tutor_form': tutor_form,
                   'user': user_obj,
                   'action': 'E'})

    #
    # user_obj = get_object_or_404(CustomUser, id=id)
    # user_form = UserEditForm(request.POST or None, instance=user_obj)
    # # if request.method == 'POST':
    # #     user_form = UserEditForm(request.POST)
    # if user_form.is_valid():
    #     print(1)
    #     new_user = user_form.save(commit=False)
    #     new_user.save()
    #     return render(request, 'account/user_result.html',
    #            {'user': new_user,
    #             'action': 'E'})
    # # else:
    # #     user_obj = get_object_or_404(CustomUser, id=id)
    # #     student_obj = Student.objects.filter(user_id=user_obj.id).first()
    # #     tutor_obj = Tutor.objects.filter(user_id=user_obj.id).first()
    # #     if student_obj:
    # #         student_obj.date_of_birth = student_obj.date_of_birth.strftime("%d.%m.%Y")
    # #     if tutor_obj:
    # #         tutor_obj.date_of_birth = tutor_obj.date_of_birth.strftime("%d.%m.%Y")
    # #     user_form = UserEditForm(instance=user_obj)
    # #     student_form = StudentAdditionalForm(instance=student_obj, prefix='std')
    # #     tutor_form = TutorAdditionalForm(instance=tutor_obj, prefix='tut')
    # # # return render(request, 'account/user_register.html', {'user_form': user_form,
    # # #                                                          'student_form': student_form,
    # # #                                                          'tutor_form': tutor_form})
    # return render(request, 'account/user_edit.html',
    #               {'user_form': user_form,
    #                'action': 'E'})


def user_delete(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    student_obj = Student.objects.filter(user_id=user_obj.id).first()
    tutor_obj = Tutor.objects.filter(user_id=user_obj.id).first()
    user = CustomUser.objects.get(id=id)

    if request.method == 'POST':
        try:
            if student_obj:
                student_obj.delete()
            if tutor_obj:
                tutor_obj.delete()
            user_obj.delete()
            return render(request, 'account/user_result.html',
                          {'user': user,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'account/user_delete_error.html',
                          {'user': user}, status=423)
    return render(request, 'account/user_delete.html', {'user': user})


def user_delete_tutor(request, id):
    tutor_obj = get_object_or_404(Tutor.objects, user_id__id=id)
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        try:
            tutor_obj.delete()
            return render(request, 'account/tutor_result.html',
                          {'user': user_obj,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'account/tutor_delete_error.html',
                          {'user': user_obj}, status=423)
    return render(request, 'account/tutor_delete.html', {'user': user_obj})


def user_delete_student(request, id):
    student_obj = get_object_or_404(Student.objects, user_id__id=id)
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        try:
            student_obj.delete()
            return render(request, 'account/student_result.html',
                          {'user': user_obj,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'account/student_delete_error.html',
                          {'user': user_obj}, status=423)
    return render(request, 'account/student_delete.html', {'user': user_obj})


def group_details(request, group_id):
    pass


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


# DISCIPLINE BLOCK


def discipline_list(request):
    disciplines = Discipline.objects.all()
    return render(request, 'discipline/discipline_list.html', {'disciplines': disciplines})


def discipline_details(request, discipline_id):
    discipline_obj = get_object_or_404(Discipline.objects, discipline_id=discipline_id)
    groups_obj = (Curriculum.objects.select_related('group_semester_id__group_id')
                  .values('group_semester_id__semester_num', 'group_semester_id__group_id__name',
                          'group_semester_id__group_id__group_id')
                  .filter(discipline_id__discipline_id=discipline_id).all())
    tutors_obj = (CurriculumLesson.objects.select_related('tutor_id__user_id')
                  .values('tutor_id__user_id__id', 'tutor_id__user_id__last_name', 'tutor_id__user_id__first_name',
                          'tutor_id__user_id__second_name')
                  .distinct()
                  .filter(curriculum_id__discipline_id__discipline_id=discipline_id).all())

    print(groups_obj.__dict__)

    context = {'discipline': discipline_obj,
               'groups': groups_obj,
               'tutors': tutors_obj
               }
    print(context)
    return render(request, 'discipline/discipline_detail.html', context)


def discipline_register(request):
    if request.method == 'POST':
        discipline_form = DisciplineRegisterForm(request.POST)
        if discipline_form.is_valid():
            new_discipline = discipline_form.save(commit=False)
            new_discipline.save()
            print(new_discipline)
            return render(request, 'discipline/discipline_result.html',
                          {'discipline': new_discipline, 'action': 'C'})
    else:
        discipline_form = DisciplineRegisterForm()
    return render(request, 'discipline/discipline_form.html',
                  {'discipline_form': discipline_form, 'action': 'C'})


def discipline_edit(request, discipline_id):
    obj = get_object_or_404(Discipline, discipline_id=discipline_id)
    print(obj)
    discipline_form = DisciplineRegisterForm(request.POST or None, instance=obj)
    if discipline_form.is_valid():
        discipline_form.save()
        print({'discipline': discipline_form,
               'action': 'E'})
        return render(request, 'discipline/discipline_result.html',
                      {'discipline': obj,
                       'action': 'E'})
    return render(request, 'discipline/discipline_form.html',
                  {'discipline_form': discipline_form,
                   'action': 'E'})


def discipline_delete(request, discipline_id):
    obj = get_object_or_404(Discipline, discipline_id=discipline_id)
    discipline = Discipline.objects.get(discipline_id=discipline_id)
    if request.method == 'POST':
        try:
            obj.delete()
            return render(request, 'discipline/discipline_result.html',
                          {'discipline': discipline,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'discipline/discipline_delete_error.html',
                          {'discipline': discipline}, status=423)
    return render(request, 'discipline/discipline_delete.html', {'discipline': discipline})


# CLASSROOM BLOCK


def classroom_list(request):
    classrooms = Classroom.objects.all()
    return render(request, 'classroom/classroom_list.html', {'classrooms': classrooms})


def classroom_details(request, classroom_id):
    context = {'classroom': Classroom.objects.get(classroom_id=classroom_id)}
    print(context)
    return render(request, 'classroom/classroom_detail.html', context)


def classroom_register(request):
    if request.method == 'POST':
        classroom_form = ClassroomRegisterForm(request.POST)
        if classroom_form.is_valid():
            new_classroom = classroom_form.save(commit=False)
            new_classroom.save()
            print(new_classroom)
            return render(request, 'classroom/classroom_detail.html',
                          {'classroom': new_classroom,
                           'action': 'C'})
    else:
        classroom_form = ClassroomRegisterForm()
    return render(request, 'classroom/classroom_form.html',
                  {'classroom_form': classroom_form,
                   'action': 'C'})


def classroom_edit(request, classroom_id):
    obj = get_object_or_404(Classroom, classroom_id=classroom_id)
    print(obj)
    classroom_form = ClassroomRegisterForm(request.POST or None, instance=obj)
    if classroom_form.is_valid():
        classroom_form.save()
        print({'classroom': classroom_form,
               'action': 'E'})
        return render(request, 'classroom/classroom_detail.html',
                      {'classroom': obj,
                       'action': 'E'})
    return render(request, 'classroom/classroom_form.html',
                  {'classroom_form': classroom_form,
                   'action': 'E'})


def classroom_delete(request, classroom_id):
    obj = get_object_or_404(Classroom, classroom_id=classroom_id)
    classroom = Classroom.objects.get(classroom_id=classroom_id)
    if request.method == 'POST':
        try:
            obj.delete()
            return render(request, 'classroom/classroom_detail.html',
                          {'classroom': classroom,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'classroom/classroom_delete_error.html',
                          {'classroom': classroom}, status=423)
    return render(request, 'classroom/classroom_delete.html', {'classroom': classroom})


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
        try:
            obj.delete()
            return render(request, 'lesson_time/lesson_time_detail.html',
                          {'lesson_time': lesson_time,
                           'action': 'D'})
        except ProtectedError:
            return render(request, 'lesson_time/lesson_time_delete_error.html',
                          {'lesson_time': lesson_time}, status=423)
    return render(request, 'lesson_time/classroom_delete.html', {'lesson_time': lesson_time})


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


def group_member_register(request):
    if request.method == 'POST':
        group_member_form = GroupMemberRegisterForm(request.POST)
        if group_member_form.is_valid():
            new_group_member = group_member_form.save(commit=False)
            new_group_member.save()
            return render(request, 'group_member/group_member_register_done.html',
                          {'group_member_form': new_group_member})
    else:
        if 'student_id' in request.GET.dict():
            obj = get_object_or_404(Student, student_id=request.GET.get('student_id'))
            group_member_form = GroupMemberRegisterForm(initial={'student_id': obj})
        else:
            group_member_form = GroupMemberRegisterForm()
    return render(request, 'group_member/group_member_register.html', {'group_member_form': group_member_form})


@transaction.atomic
def curriculum_register(request):
    new_curriculum = None
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
        if 'discipline_id' in request.GET.dict():
            obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            curriculum_form = CurriculumRegisterForm(initial={'discipline_id': obj})
        else:
            curriculum_form = CurriculumRegisterForm()
    return render(request, 'curriculum/curriculum_from.html', {'curriculum_form': curriculum_form})


def curriculum_lesson_register(request):
    discipline_obj = None
    if request.method == 'POST':
        curriculum_lesson_form = CurriculumLessonRegisterForm(request.POST)
        if curriculum_lesson_form.is_valid():
            new_curriculum_lesson = curriculum_lesson_form.save(commit=False)
            new_curriculum_lesson.save()
            return render(request, 'curriculum_lesson/curriculum_lesson_register_done.html',
                          {'curriculum_lesson_form': new_curriculum_lesson})
    else:
        if 'tutor_id' in request.GET.dict():
            obj = get_object_or_404(Tutor, tutor_id=request.GET.get('tutor_id'))
            curriculum_lesson_form = CurriculumLessonRegisterForm(initial={'tutor_id': obj})
        if 'discipline_id' in request.GET.dict():
            discipline_obj = get_object_or_404(Discipline, discipline_id=request.GET.get('discipline_id'))
            curriculums_obj = Curriculum.objects.filter(discipline_id=request.GET.get('discipline_id')).all()
            curriculum_lesson_form = CurriculumLessonRegisterForm(initial={'discipline_id': discipline_obj})
            curriculum_lesson_form.set_initial_curriculum_ids(curriculums_obj)
        else:
            curriculum_lesson_form = CurriculumLessonRegisterForm()
    return render(request, 'curriculum_lesson/curriculum_lesson_register.html',
                  {'curriculum_lesson_form': curriculum_lesson_form,
                   'discipline': discipline_obj})


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
