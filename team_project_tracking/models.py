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
STATUS_CHOICES=(
        ('active', 'active'),
        ('archive', 'archive'),
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
    # def get_absolute_url(self):
    #     return reverse('course_details', args=[self.id])
    def get_absolute_url(self):
        return reverse('course_details', args=[str(self.id)])
    def __str__(self):
        return self.course_name


class Role(models.Model):
    role_title = models.CharField(unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'role'

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