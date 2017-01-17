from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^participant/register/?$', views.register),
    url(r'^participant/login/?$', views.login),
    url(r'^team/new/?$', views.register_team, name='register-team'),
]