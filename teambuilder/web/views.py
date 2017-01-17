from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.utils import timezone

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


def register_team(request):
	user = utils.get_login_user(request.COOKIES)
	error = []
	if user:
		if request.POST.get('register', None):
			team_name = request.POST.get('name')
			# spaces are replaced by '-' due to security reasons
			team_name = team_name.replace(' ', '-', 32)
			description = request.POST.get('description')
			created_by = user
			created_time = timezone.now()
			try:
				with atomic():
					team = models.Team.objects.create(name=team_name, created_by=created_by, create_time=created_time,
													  description=description)
					team.save()
					return HttpResponseRedirect('/')
			except Exception as e:
				print(e)
				error.append("failed to create team - {0}".format(e))
	else:
		error.append("Please login to create team")
	return render(
		request, 'register_team.html', context={
			'title': 'register your team',
			'errors': error,
			'user': None,
		})


def teams(request):
	team = models.Team.objects.all()
	return render(
		request, 'teams.html', context={
			'title': 'Teams',
			'teams': team,
		})


def team_profile(request, team_name):
	try:
		team = models.Team.objects.get(name=team_name)
	except ObjectDoesNotExist:
		print("No team found with this name")
		return HttpResponse('404 not found')
	members = models.TeamMember.objects.filter(team=team)
	return render(
		request, 'team_profile.html', context={
			'team': team,
			'members': members
		})


def participant(request):
	participants = models.Participant.objects.all()
	return render(
		request, 'participant.html', context={
			'participants':participants
		})
