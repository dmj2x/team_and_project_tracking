from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import MaxValueValidator, MinValueValidator
from bootstrap_datepicker_plus import DatePickerInput
from django.core.exceptions import PermissionDenied
from team_project_tracking.models import Profile, Course, SEX_CHOICES, SEMESTER_CHOICES
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
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('Email address already registered!')
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control col-6 col-md-4',
                'autofocus': '',
            }
        ))


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


# def current_year():
#     return date.today().year
# def year_choices():
#     return [(r,r) for r in range(2010, date.today().year+5)]


# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['course_name', 'course_number', 'course_description', 'semester', 'year']
#     course_name = forms.CharField(
#         label='Course Name',
#         max_length=100,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control col-6 col-md-4',
#                 'autofocus': '',
#                 'placeholder': 'enter course name',
#             }
#         ), )
#     course_number = forms.CharField(
#         label='Course Number',
#         required=False,
#         widget=forms.CharField(
#             attrs={
#                 'class':'form-control col-6 col-md-4',
#                 'autofocus': '',
#                 'placeholder': 'enter course number',
#             }
#         ),)
#     course_description = forms.CharField(
#         label='Course Description',
#         required=False,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control col-6 col-md-4',
#                 'autofocus': '',
#                 'placeholder': 'enter course description',
#             }
#         ),)
#     semester = forms.ChoiceField(
#         label='Semester',
#         coerce=str,
#         required=True,
#         choices=SEMESTER_CHOICES,
#         widget=forms.Select(
#             attrs={
#                 'class':'form-control col-6 col-md-4',
#                 'autofocus': '',
#             }
#         ),)
#     year = forms.TypedChoiceField(
#         label='Year',
#         coerce=str,
#         required=False,
#         choices=year_choices,
#         initial=current_year,
#         widget=forms.Select(
#             attrs={
#                 'class':'form-control col-6 col-md-4',
#                 'autofocus': '',
#             }
#         ),)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     course_name = cleaned_data.get('course_name')
    #     course_number = cleaned_data.get('course_number')
    #     course_description = cleaned_data.get('course_description')
    #     semester = cleaned_data.get('semester')
    #     year = cleaned_data.get('year')