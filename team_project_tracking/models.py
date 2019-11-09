from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from partial_date import PartialDateField
from django.utils import timezone
from decouple import config
from datetime import datetime, timezone, timedelta, date
from django.contrib.auth.models import User


NAN = '-'
MALE = 'M'
FEMALE = 'F'
SEX_CHOICES = (
    (NAN, '---'),
    (FEMALE, 'Female'),
    (MALE, 'Male'),
)
SEMESTER_CHOICES=(
    ('--', '--'),
    ('fall', 'fall'),
    ('spring', 'spring'),
    ('summer', 'summer'),
)
TEAM_STATUS_CHOICES=(
    ('pending', 'pending'),
    ('active', 'active'),
    ('inactive', 'inactive'),
)
PROJECT_STATUS_CHOICES=(
    ('in-progress', 'in-progress'),
    ('complete', 'complete'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'profile'
    # def __str__(self):
    #     return "%s" % self.user.get_full_name


class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False, null=False)
    course_number = models.CharField(max_length=12, null=False, blank=False)
    course_description = models.TextField(null=True, blank=True)
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES, null=False, blank=False, default='--')
    year = PartialDateField(null=False, blank=False)
    # status = models.models.CharField(max_length=6, choices=STATUS_CHOICES, null=False, blank=False, default='active')

    class Meta:
        db_table = 'course'
        unique_together = (('course_name', 'semester', 'year'),)
    def get_absolute_url(self):
        return reverse('course_details', args=[str(self.id)])
    def __str__(self):
        return self.course_name


class Role(models.Model):
    role_title = models.CharField(unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'role'
    def get_absolute_url(self):
        return reverse('role_details', args=[str(self.id)])
    def __str__(self):
        return self.role_title


class UserRole(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE,
                                    null=False, related_name='user_role', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=False, related_name='user_with_role', blank=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE,
                                    null=False, related_name='user_course_role', blank=False)

    class Meta:
        db_table = 'user_role'
        unique_together = (('role', 'user', 'course'),)
    def __str__(self):
        return '%s for %s in %s' % (self.role, self.user, self.course)


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=False, null=False)
    team_status = models.CharField(max_length=10, choices=TEAM_STATUS_CHOICES, 
                                    null=False, blank=False, default='pending')
    course = models.OneToOneField('Course', on_delete=models.CASCADE,
                                    null=False, related_name='team_course', blank=False)
    team_creator = models.OneToOneField(User, on_delete=models.CASCADE,
                                    null=False, related_name='team_creator', blank=False)

    class Meta:
        db_table = 'team'
        unique_together = (('team_name', 'course', 'team_creator'),)
    def get_absolute_url(self):
        return reverse('team_details', args=[str(self.id)])
    def __str__(self):
        return self.team_name


# class TeamProject(models.Model):
#     team = models.ForeignKey('Team', on_delete=models.CASCADE,
#                                     null=False, related_name='team_with_project', blank=False)
#     project_name = models.CharField(blank=False, null=False, max_length=100)
#     description = models.TextField(blank=True, null=True)
#     project_status = models.CharField(max_length=15, choices=PROJECT_STATUS_CHOICES, 
#                                     null=False, blank=False, default='in-progress')
    
#     class Meta:
#         db_table = 'team_project'
#         unique_together = (('team', 'project_name'),)
#     def get_absolute_url(self):
#         return reverse('team_project_details', args=[str(self.id)])
#     def __str__(self):
#         return 'Project %s for team %s' % (self.project_name, self.team)


class TeamMember(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE,
                                    null=False, related_name='team_with_member', blank=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=False, related_name='member_with_team', blank=False)
    team_leader = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'team_member'
        unique_together = (('team', 'member'),)
    def __str__(self):
        return '%s is a member %s' % (self.member, self.team)