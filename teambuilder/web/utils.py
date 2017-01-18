from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


def get_login_user(cookie):
    user_id = cookie.get('username', None)
    if not user_id:
        return None
    users = models.Participant.objects.filter(user__username=user_id)
    if len(users) == 0:
        return None
    return users[0]


@receiver(post_save, sender=models.Participant)
def create_payment(sender, instance=None, created=False, **kwargs):
    if created:
        # Auto create payment instance for the user and default it to False
        # i.e., he has not made the payment yet
        payment_model = models.Payment(user=instance)
        payment_model.save()
        # Auto create skill instance for the user
        skill = models.Skill(participant=instance)
        skill.save()


def verify_skills(skills):
    try:
        for skill in skills:
            x = int(skill)
            if x < 0 or x > 10:
                return False
    except ValueError:
        return False
    return True
