import traceback

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.transaction import atomic

from . import models
from . import utils


def home(request):
    user = utils.get_login_user(request.COOKIES)
    if user is None:
        if request.COOKIES.get('username', None):  # Unknown user
            response = redirect('/participant/login')
            response.set_cookie(key='username', value='', expires=0)
            return response
    announcements = models.Announcement.objects.order_by('-create_time')[:5]
    return render(request, 'home.html', context={
        'title': 'Hackathon 2017 | Home',
        'user': user,
        'announcements': announcements,
    })


def register(request):
    # TODO: Make tests more effective
    user = utils.get_login_user(request.COOKIES)
    if user:
        return redirect('/')
    error = []
    if request.POST.get('register', None):
        student_id = request.POST.get('student_id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        mobile = request.POST.get('mobile')

        if len(password) >= 8:
            if password == password_repeat:
                try:
                    with atomic():
                        user = User.objects.create_user(
                            username=student_id, email=email,
                            password=password)
                        user.first_name = firstname
                        user.last_name = lastname
                        user.save()
                        participant = models.Participant(user=user,
                                                         mobile=mobile)
                        participant.save()
                        response = redirect('/')
                        response.set_cookie(key='username',
                                            value=participant.user.username)
                        return response
                except Exception as e:
                    error.append('Unable to create user - {0}'.format(e))
                    traceback.print_exc()
            else:
                error.append('Passwords do not match')
        else:
            error.append('Password length should be greater than 8')
        if password != password_repeat:
            error.append('Passwords do not match')

    return render(request, 'register.html', context={
        'title': 'Hackathon 2017 | Register',
        'errors': error,
        'user': None,
    })


def login(request):
    # TODO: Add better checks
    user = utils.get_login_user(request.COOKIES)
    if user:
        return redirect('/')
    error = []
    if request.POST.get('login', None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_users = User.objects.filter(username=username)
        if len(login_users) > 0:
            login_user = login_users[0]
            if login_user.check_password(password):
                response = redirect('/')
                response.set_cookie(key='username', value=login_user.username)
                return response
        error.append('No such user found')
    return render(request, 'login.html', context={
        'title': 'Hackathon 2017 | Login',
        'user': None,
        'errors': error
    })


def participant_show(request, username):
    user = utils.get_login_user(request.COOKIES)
    participant = models.Participant.objects.filter(user__username=username)
    if len(participant) == 0:
        return render(request, '404.html', context={
            'title': 'The participant you are looking for was not found.',
            'user': user,
            'message': 'No participant found for ID {0}'.format(username),
        }, status=404)
    participant = participant[0]
    own_page = participant == user
    return render(request, 'participant_show.html', context={
        'title': 'Hackathon 2017 | Participant | {0} {1}'.format(
            participant.user.first_name, participant.user.last_name),
        'user': user,
        'participant': participant,
        'own_page': own_page,
        'skills': participant.get_skills(),
        'payment': participant.get_payment_status(),
        'team': participant.get_team(),
    })


def edit_participant(request):
    user = utils.get_login_user(request.COOKIES)
    if not user:
        redirect('/participant')
    error = []
    if request.POST.get('save', None):  # User has made some changes
        try:
            valid_credentials = True
            first_name = request.POST.get('first_name')
            if len(first_name) > 30:
                valid_credentials = False
                error.append('First name should be at most 30 characters.')
            last_name = request.POST.get('last_name')
            if len(last_name) > 30:
                valid_credentials = False
                error.append('Last name should be at most 30 characters.')
            mobile = request.POST.get('mobile')
            try:
                if len(mobile) != 10:
                    raise ValueError()
                int(mobile)
            except ValueError:
                valid_credentials = False
                error.append('Invalid mobile number.')
            email = request.POST.get('email')
            front_end = request.POST.get('front_end')
            back_end = request.POST.get('back_end')
            testing = request.POST.get('testing')
            managing = request.POST.get('managing')
            presentation = request.POST.get('presentation')
            valid_skills = utils.verify_skills([front_end, back_end, testing,
                                                     managing, presentation])
            if not valid_skills:
                error.append('Invalid points for one or more skills.')
                valid_credentials = False
            if valid_credentials:
                with atomic():
                    user.user.first_name = first_name
                    user.user.last_name = last_name
                    user.mobile = mobile
                    user.user.email = email
                    user.user.save()
                    user.save()
                    skill = user.get_skills()
                    skill.front_end = int(front_end)
                    skill.back_end = int(back_end)
                    skill.testing = int(testing)
                    skill.managing = int(managing)
                    skill.presentation = int(presentation)
                    skill.save()
                return redirect('/participant/profile/edit')
        except Exception:
            error.append('Unknown problem occurred')
            traceback.print_exc()
    skill = user.get_skills()
    return render(request, 'edit_participant.html', context={
        'title': 'Hackathon 2017 | Participant | Edit Profile',
        'user': user,
        'skill': skill,
        'errors': error,
    })


def announcements(request):
    user = utils.get_login_user(request.COOKIES)
    announcement = models.Announcement.objects.order_by('-create_time')
    print(announcement)
    return render(request, 'announcements.html', context={
        'title': 'Hackathon 2017 | Announcements',
        'announcements': announcement,
        'user': user,
    })
