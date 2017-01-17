from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.transaction import atomic

from . import models
from . import utils


def home(request):
    user = utils.get_login_user(request.COOKIES)
    if user is None:
        return redirect('/participant/login')
    return render(request, 'home.html', context={
        'title': 'Welcome to Hackathon 2017',
        'user': user,
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
            else:
                error.append('Passwords do not match')
        else:
            error.append('Password length should be greater than 8')
        if password != password_repeat:
            error.append('Passwords do not match')
    else:
        error.append('Nothing provided')

    return render(request, 'register.html', context={
        'title': 'Register for Hackathon 2017',
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
        'title': 'Login',
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
        'payment': participant.get_payment_status()
    })
