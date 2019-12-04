from django.contrib.postgres.fields import JSONField
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
    ('pending-approval', 'pending-approval'),
    ('active', 'active'),
    ('inactive', 'inactive'),
)
PROJECT_STATUS_CHOICES=(
    ('in-progress', 'in-progress'),
    ('complete', 'complete'),
)
COURSE_STATUS_CHOICES=(
    ('active', 'active'),
    ('discontinued', 'discontinued'),
)
STUDENT_ROLE_CHOICES=(
    ('student', 'student'),
    ('teaching-assistant', 'teaching-assistant'),
)
STUDENT_STATUS_CHOICES=(
    ('pending-approval', 'pending-approval'),
    ('approved', 'approved'),
    ('decined', 'declined'),
)

def get_first_name(self):
    if (self.first_name and self.last_name):
        return '%s %s' % (self.first_name, self.last_name)
    elif (self.first_name):
        return self.first_name
    elif (self.last_name):
        return self.last_name
    elif (self.username):
        return self.username
    else:
        return self.email

User.add_to_class("__str__", get_first_name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=25, blank=True, null=True)
    
    class Meta:
        db_table = 'profile'
    # def __str__(self):
    #     return "%s" % self.user.get_full_name


class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False, null=False)
    course_number = models.CharField(max_length=12, null=False, blank=False)
    course_description = models.TextField(null=True, blank=True)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, 
                                        null=False, related_name='faculty', blank=False)

    class Meta:
        db_table = 'course'
    def get_absolute_url(self):
        return reverse('course_details', args=[str(self.id)])
    def __str__(self):
        return self.course_name


class CourseOffering(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE,
                                    null=False, related_name='course', blank=False)
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES, null=False, blank=False, default='--')
    year = PartialDateField(null=False, blank=False)
    course_status = models.CharField(max_length=10, choices=COURSE_STATUS_CHOICES, null=False, blank=False, default='active')
    
    class Meta:
        db_table = 'course_offering'
        unique_together = (('course', 'semester', 'year'),)
        # indexes = [
        #     models.Index(fields=['course', 'semester', 'year'])
        # ]
    # def get_absolute_url(self):
    #     return reverse('course_details', args=[str(self.id)])
    def __str__(self):
        return '%s, %s%s' % (self.course, self.semester, self.year)



class CourseStudent(models.Model):
    course_offering = models.ForeignKey('CourseOffering', on_delete=models.CASCADE,
                                    null=False, related_name='course_offering', blank=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=True, related_name='student', blank=True)
    student_role = models.CharField(max_length=20, choices=STUDENT_ROLE_CHOICES, 
                                    null=False, blank=False, default='student')
    student_status = models.CharField(max_length=20, choices=STUDENT_STATUS_CHOICES, 
                                    null=False, blank=False, default='pending-approval')
    
    class Meta:
        db_table = 'course_student'
        unique_together = (('course_offering', 'student', 'student_role'),)
        # indexes = [
        #     models.Index(fields=['course_offering', 'student'])
        # ]
    def __str__(self):
        return '%s is a student in %s' % (self.student, self.course_offering)


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

    class Meta:
        db_table = 'user_role'
        unique_together = (('role', 'user',),)
        indexes = [
            models.Index(fields=['role', 'user',])
        ]
    def __str__(self):
        return '%s is %s' % (self.user, self.role)


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=False, null=False)
    team_status = models.CharField(max_length=18, choices=TEAM_STATUS_CHOICES, 
                                    null=False, blank=False, default='pending')
    course_offering = models.ForeignKey('CourseOffering', on_delete=models.CASCADE,
                                    null=False, related_name='team_course_offering', blank=False)

    class Meta:
        db_table = 'team'
        unique_together = (('team_name', 'course_offering'),)
        indexes = [
            models.Index(fields=['team_name', 'course_offering'])
        ]
    def get_absolute_url(self):
        return reverse('team_details', args=[str(self.id)])
    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE,
                                    null=False, related_name='team_with_member', blank=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=False, related_name='member_with_team', blank=False)
    team_leader = models.BooleanField(null=True, blank=True, default=False)
    team_creator = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = 'team_member'
        unique_together = (('team', 'member'),)
    def __str__(self):
        return '%s is a member %s' % (self.member, self.team)


class TeamProject(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE,
                                    null=False, related_name='team_with_project', blank=False)
    project_name = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(auto_now=False, blank=True, null=True)
    project_status = models.CharField(max_length=15, choices=PROJECT_STATUS_CHOICES, 
                                    null=False, blank=False, default='in-progress')
    
    class Meta:
        db_table = 'team_project'
        unique_together = (('team', 'project_name'),)
    def get_absolute_url(self):
        return reverse('team_project_details', args=[str(self.id)])
    def __str__(self):
        return 'Project %s for team %s' % (self.project_name, self.team)


class ProjectUpdate(models.Model):
    project = models.ForeignKey('TeamProject', on_delete=models.CASCADE,
                                    null=False, related_name='project_update')
    update_title = models.CharField(null=False, blank=False, max_length=20)
    update_notes = models.TextField(blank=True)
    date = models.DateField(auto_now=False, blank=False, null=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'project_update'
        unique_together = (('project', 'update_title'),)
    def __str__(self):
        return self.update_title
    @property
    def save_model(self):
        user = get_user_model()
        obj.created_by = user.username
        super().save_model()