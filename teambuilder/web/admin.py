from django.contrib import admin

from . import models

admin.site.register([models.Payment, models.Participant, models.Skill,
                     models.Team, models.TeamJoinRequest, models.TeamMember,
                     models.Announcement])
