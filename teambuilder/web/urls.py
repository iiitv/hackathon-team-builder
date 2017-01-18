from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^participant/register/?$', views.register),
    url(r'^participant/login/?$', views.login),
    url(r'participant/profile/edit/?', views.edit_participant),
    url(r'^participant/profile/(?P<username>[0-9]{9})/?$',
        views.participant_show),
    url(r'^announcements/?$', views.announcements)
]