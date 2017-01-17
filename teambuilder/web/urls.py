from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^participant/register/?$', views.register, name='register'),
    url(r'^participant/login/?$', views.login, name='login'),
    url(r'^team/new/?$', views.register_team, name='register-team'),
    url(r'^team/?$', views.teams, name='view-teams'),
    url(r'^participant/?$', views.participant, name='view-participants'),
    url(r'^team/profile/(?P<team_name>[\S]+)/?$', views.team_profile, name='team-profile'),
]