from django.db import models
from django.utils import timezone


class Participant(models.Model):

    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1024, default='', blank=False,
                            null=False)
    join_time = models.DateTimeField(default=timezone.now)


class Skill(models.Model):

    student = models.ForeignKey(Participant)
    front_end = models.PositiveIntegerField(default=0, null=False)
    back_end = models.PositiveIntegerField(default=0, null=False)
    managing = models.PositiveIntegerField(default=0, null=False)
    marketing = models.PositiveIntegerField(default=0, null=False)
    # TODO: Verify


class Team(models.Model):

    name = models.CharField(primary_key=True, max_length=64)
    create_time = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Participant)


class TeamMember(models.Model):

    team = models.ForeignKey(Team)
    member = models.ForeignKey(Participant, related_name='member')
    add_time = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(Participant, related_name='added_by')


class TeamJoinRequest(models.Model):

    team = models.ForeignKey(Team)
    member = models.ForeignKey(Participant)
    request_time = models.DateTimeField(default=timezone.now)
