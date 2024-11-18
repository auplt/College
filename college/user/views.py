"""
Views for user app.
"""

from django.urls import reverse, resolve, Resolver404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import CustomUser, Tutor, Student
from group.models import GroupMember
from curriculum.models import CurriculumLesson
from .forms import UserRegistrationForm, UserEditForm, StudentAdditionalForm, TutorAdditionalForm
from timetable.views import tt_lesson_details


@login_required
def home(request):
    """
    View that redirects to home page.
    :param request: user's request
    :return: HTTP response HTML page with home page
    """
    if 'next' in request.GET.keys():
        try:
            next_url = request.GET.get('next')
            if ':' in next_url:
                next_url = next_url.replace(':', '&')
            print(next_url)
            resolve_match = resolve(next_url)

            return redirect(next_url)

        except Resolver404 or KeyError:
            return HttpResponseRedirect(reverse('user:user_details', args=[request.user.id]))

        # resolve_match = resolve(request.GET.get('next'))
        # return redirect(request.GET.get('next'))
    else:
        return HttpResponseRedirect(reverse('user:user_details', args=[request.user.id]))


def welcome(request):
    """
    View for welcome page.
    :param request: user's request
    :return: HTTP response plug HTML page
    """
    return render(request,
                  'user/welcome.html')


# USER BLOCK

def user_list(request):
    """
    View for list of users.
    :param request: user's request
    :return: HTTP response HTML page with users list
    """
    print(request.user.get_all_permissions())
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
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/user_list.html', context=context)


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
        .values('group_member_id',
                'group_semester_id__group_id__name',
                'group_semester_id__semester_num',
                'group_semester_id__group_id__group_id') \
        .filter(student_id__user_id__id=id) \
        .all()

    disciplines = CurriculumLesson.objects.select_related('tutor_id__user_id',
                                                          'curriculum_id__discipline_id') \
        .values(
        # 'curriculum_lesson_id',
        'curriculum_id__discipline_id__name',
        'curriculum_id__discipline_id__discipline_id') \
        .filter(tutor_id__user_id__id=id) \
        .distinct() \
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
    context.update(tt_lesson_details(request, user_id=id))
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    print(context)
    return render(request, 'user/user_details.html', context=context)


@permission_required('user.add_customuser', raise_exception=True)
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
                return redirect(reverse('user:user_list'))
    else:
        user_form = UserRegistrationForm()
        student_form = StudentAdditionalForm(False, prefix='std')
        tutor_form = TutorAdditionalForm(False, prefix='tut')
    context = {'user_form': user_form,
               'student_form': student_form,
               'tutor_form': tutor_form,
               'action': 'C'}
    print(user_form)
    print(student_form)
    print(tutor_form)
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/user_register.html', context=context)


@permission_required('user.change_customuser', raise_exception=True)
@transaction.atomic
def user_edit(request, id):
    print(request.user.get_all_permissions())
    """
    View for registering user.
    :param request: user's request
    :return: HTTP response HTML page with register form
    """
    if request.user.id != id and not request.user.is_superuser:
        raise PermissionDenied()

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
                    return redirect(reverse('user:user_details', kwargs={'id': id}))
                # return render(request, 'user/register_done.html', {'new_user': new_user})
    # else:
    #     user_form = UserRegistrationForm()
    #     student_form = StudentAdditionalForm(False, prefix='std')
    #     tutor_form = TutorAdditionalForm(False, prefix='tut')
    # return render(request, 'user/user_register.html', {'user_form': user_form,
    #                                                          'student_form': student_form,
    #                                                          'tutor_form': tutor_form})

    context = {'user_form': user_form,
               'student_form': student_form,
               'tutor_form': tutor_form,
               'user': user_obj,
               'student': student_obj,
               'tutor': tutor_obj,
               'action': 'U'}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/user_edit.html', context=context)


@permission_required('user.delete_customuser', raise_exception=True)
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
                return redirect(reverse('user:user_list'))
        except Http404:
            return redirect(reverse('user:user_list'))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('user:user_details', kwargs={'id': id}))
    context = {'user': user}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/user_delete.html', context=context)


@permission_required('user.delete_tutor', raise_exception=True)
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
                return redirect(reverse('user:user_details', kwargs={'id': id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('user:user_details', kwargs={'id': id}))
    context = {'user': user_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/tutor_delete.html', context=context)


@permission_required('user.delete_student', raise_exception=True)
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
                return redirect(reverse('user:user_details', kwargs={'id': id}))
        except ProtectedError:
            request.session["obj_status"] = 'error'
            try:
                resolve_match = resolve(request.GET.get('next'))
                return redirect(request.GET.get('next'))
            except Resolver404 or KeyError or Http404:
                return redirect(reverse('user:user_details', kwargs={'id': id}))
    context = {'user': user_obj}
    if 'next' in request.GET.keys():
        context['next_url'] = request.GET.get('next')
    return render(request, 'user/student_delete.html', context=context)
