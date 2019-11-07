from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from team_project_tracking.models import Role

from django.utils import timezone

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def add_to_default_group(sender, instance, created, **kwargs):
#     if created:
#         permissions_list = Permission.objects.filter(
#                 Q(name__contains='Can view community') |
#                 Q(name__contains='Can view project') |
#                 Q(name__contains='Can view funding') |
#                 Q(name__contains='Can view member'))
#         instance.user_permissions.set(permissions_list)
#         accepted_email = instance.email
#         if UserInvitation.objects.filter(email=accepted_email).exists():
#             user_invited = UserInvitation.objects.get(email=accepted_email)
#             user_invited.invitation_status = 'accepted'
#             user_invited.accepte_date = timezone.now()
#             user_invited.save()
#         else:
#             pass
