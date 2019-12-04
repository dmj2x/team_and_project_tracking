from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import MaxValueValidator, MinValueValidator
from bootstrap_datepicker_plus import DatePickerInput
from django.core.exceptions import PermissionDenied
from team_project_tracking.models import *
from datetime import date
import logging


User = get_user_model()
logger = logging.getLogger(__name__)


class UserLoginForm(forms.Form):
    required_css_class = 'required'
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'enter your email',
            }
    ), )

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'enter password',
            }
    ), )
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user_with_email = User.objects.get(email=email)
                username=user_with_email.get_username()
                user = authenticate(username=username, password=password)
                if not user_with_email.is_active:
                    raise PermissionDenied
                elif not user:
                    raise forms.ValidationError('incorrect email or passoword')
                elif not user.check_password(password):
                    raise forms.ValidationError('incorrect email or passoword!')
                elif not user.is_active:
                    raise PermissionDenied
            except User.DoesNotExist:
                logger.debug("*****An unauthorized user with email '%s', tried to login!****", email)
                raise PermissionDenied
                # raise forms.ValidationError('you don\'t have permission to access this system')


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'style': 'width:66ch',
                'placeholder': 'enter your first name',
            }
    ), )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter your last name',
            }
    ), )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'email address',
            }
    ), )
    confirm_email = forms.EmailField(
        label='Confirm Email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'confirm email address',
            }
    ), )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'enter password',
            }
    ), )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'placeholder': 'comfirm password',
            }
    ),)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'confirm_email', 'password', 'confirm_password',]

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        split_email = email.split('@')
        if (split_email[1].lower() != 'louisville.edu'):
            raise forms.ValidationError('you must use your lousiville.edu email to register')
        if email != confirm_email:
            raise forms.ValidationError('Email addresses must match!')
        try:
            email_qs = User.objects.filter(email=email)
            if email_qs.exists():
                raise forms.ValidationError('Email address already registered!')
        except Exception as e:
            print(e)
        if password != confirm_password:
            raise forms.ValidationError('please make sure the passwords are matching!')


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'style': 'width:66ch',
                'placeholder': 'enter your first name',
            }
    ), )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter your last name',
            }
    ), )
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    # def clean(self):
    #     super().clean()
    #     first_name = self.cleaned_data.get('first_name')
    #     last_name = self.cleaned_data.get('last_name')


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_title']
    role_title = forms.CharField(
    label='Role Title',
    max_length=100,
    widget=forms.TextInput(
    attrs={
        'class': 'form-control col-6 col-md-4',
        'autofocus': '',
        'placeholder': 'enter role title',
    }
    ), )
    description = forms.CharField(
    label='Role Description',
    required=False,
    widget=forms.Textarea(
    attrs={
        'class': 'form-control col-6 col-md-4',
        'autofocus': '',
        'placeholder': 'enter role description',
    }
    ))

    def clean(self):
        cleaned_data = super().clean()
        role_title = cleaned_data.get('role_title')
        description = cleaned_data.get('description')


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['role', 'user']
        labels = {
            'user': 'User',
            'role': 'Role',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control col-6 col-md-4'}),
            'role': forms.Select(attrs={'class': 'form-control col-6 col-md-4'}),
        }


class UpdateUserInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'style': 'width:66ch',
                'placeholder': 'enter your first name',
            }
    ), )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter your last name',
            }
    ), )

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    # def clean(self):
    #     super().clean()
    #     first_name = self.cleaned_data.get('first_name')
    #     last_name = self.cleaned_data.get('last_name')


def current_year():
    return date.today().year
def year_choices():
    return [(r,r) for r in range(2010, date.today().year+2)]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_number', 'course_description', 'faculty']
        labels = {
            'faculty': 'Faculty',
        }
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control col-6 col-md-4'}),
        }
    course_name = forms.CharField(
        label='Course Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter course name',
            }
    ), )
    course_number = forms.CharField(
        label='Course Number',
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class':'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter course number'
            }
        ),)
    course_description = forms.CharField(
        label='Course Description',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter course description',
            }
        ),)

    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get('course_name')
        course_number = cleaned_data.get('course_number')
        course_description = cleaned_data.get('course_description')


class CourseOfferingForm(forms.ModelForm):
    class Meta:
        model = CourseOffering
        fields = ['semester', 'year']
    semester = forms.ChoiceField(
        label='Semester',
        choices=SEMESTER_CHOICES,
        widget=forms.Select(
            attrs={
                'class':'form-control col-6 col-md-4',
                'autofocus': '',
            }
        ),)
    year = forms.TypedChoiceField(
        label='Year',
        coerce=str,
        required=True,
        choices=year_choices,
        initial=current_year,
        widget=forms.Select(
            attrs={
                'class':'form-control col-6 col-md-4',
                'autofocus': '',
            }
        ),)

    def clean(self):
        cleaned_data = super().clean()
        semester = cleaned_data.get('semester')
        year = cleaned_data.get('year')


class JoinCourseForm(forms.ModelForm):
    class Meta:
        model = CourseStudent
        fields = ['course_offering']
        labels = {
            'course_offering': 'Course',
        }
        widgets = {
            'course_offering': forms.Select(attrs={'class': 'form-control col-6 col-md-4'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        course_offering = cleaned_data.get('course_offering')


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'course_offering']
        labels = {'course': 'Select your course'}
        widgets = {
            'course_offering': forms.Select(attrs={
                'class': 'form-control col-6 col-md-4',
            }),
        }
    team_name = forms.CharField(
        label='Team Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter team name',
            }
    ), )

    def clean(self):
        cleaned_data = super().clean()
        team_name = cleaned_data.get('team_name')
        course = cleaned_data.get('course')


class UpdateTeamInfoForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'course_offering']
        labels = {'course_offering': 'Course'}
        widgets = {
            'course_offering': forms.Select(attrs={
                'class': 'form-control col-6 col-md-4',
            }),
        }
    team_name = forms.CharField(
        label='Team Name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
                'placeholder': 'enter team name',
            }
    ), )
    
    def clean(self):
        cleaned_data = super().clean()
        team_name = cleaned_data.get('team_name')
        course_offering = cleaned_data.get('course_offering')