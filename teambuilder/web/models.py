from django.db import models
from django.utils import timezone
from django.conf import settings


class Participant(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True)

    def get_skills(self):
        skills = Skill.objects.filter(participant=self)
        if len(skills) == 0:
            return None
        else:
            return skills[0]

    def get_payment_status(self):
        return Payment.objects.get(user=self).status

    def get_team(self):
        team = TeamMember.objects.filter(member=self)
        if len(team) == 0:
            return None
        return team[0].team


class Skill(models.Model):

    participant = models.ForeignKey(Participant)
    front_end = models.PositiveIntegerField(default=0, null=False)
    back_end = models.PositiveIntegerField(default=0, null=False)
    testing = models.PositiveIntegerField(default=0, null=False)
    managing = models.PositiveIntegerField(default=0, null=False)
    presentation = models.PositiveIntegerField(default=0, null=False)
    # TODO: Verify


class Team(models.Model):

    name = models.CharField(primary_key=True, max_length=64)
    create_time = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Participant)
    description = models.CharField(max_length=200, blank=True)

    @staticmethod
    def count():
        return Team.objects.count()


class TeamMember(models.Model):

    team = models.ForeignKey(Team)
    member = models.ForeignKey(Participant, related_name='member')
    add_time = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(Participant, related_name='added_by')


class TeamJoinRequest(models.Model):

    team = models.ForeignKey(Team)
    member = models.ForeignKey(Participant)
    request_time = models.DateTimeField(default=timezone.now)


class Payment(models.Model):

    user = models.ForeignKey(Participant)
    status = models.BooleanField(default=False)


class Announcement(models.Model):

    announcement = models.TextField(max_length=500)
    create_time = models.DateTimeField(default=timezone.now)
