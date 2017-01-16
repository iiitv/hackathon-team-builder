from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^participant/register/?$', views.register),
    url(r'^participant/login/?$', views.login),
]