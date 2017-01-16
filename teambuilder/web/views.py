from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import models


def home(request):
    user_id = request.COOKIES.get('userid', None)
    user = models.Participant.objects.filter(student_id=user_id) if user_id \
        else None
    return render(request, 'home.html', context={
        'title': 'Welcome to Hackathon 2017',
        'user': user,
    })
