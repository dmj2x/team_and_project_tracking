from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import FormView, RedirectView, TemplateView
from django.contrib.auth.views import (
		PasswordResetView, PasswordResetDoneView,
		PasswordResetConfirmView, PasswordResetCompleteView)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from team_project_tracking.forms import *
from team_project_tracking.models import *
from django.contrib.auth.forms import PasswordChangeForm
from decouple import config
import logging


# User = get_user_model()
logger = logging.getLogger(__name__)

def landing_page(request):
	""" function returns the landing page for all unauthenticated users """
	return render(request, 'welcome.html')


@login_required
def help_page(request):
	""" function returns the help with support information to guide users on how to use the system """
	return render(request, 'help_page.html')


def login_view(request):
	"""
		- function accepts get and post requests
		GET: return user login form
		POST:
			- authenticates user if both email and password are valid
			- redirects to the next page or home page
	"""
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		try:
			user_with_email = User.objects.get(email=email)
			user = authenticate(username=user_with_email.get_username(), password=password)
			login(request, user)
			messages.success(request, 'You\'re logged in!')
			if next:
				return redirect(request, next)
			return redirect('home')
		except ObjectDoesNotExist:
			logger.error("non identified user tried to login into the system")
			messages.error(request, 'you don\'t permission to access this system')
			return redirect(request, 'landing_page')
	return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
	"""
		function accepts get requests
		deauthenticates current user
	"""
	try:
		user_profile = request.user.profile
		user_profile.last_logout = datetime.now()
		user_profile.save()
	except Exception as e:
		user_info = User.objects.get(pk=request.user.id)
		user_profile = Profile(user=user_info, last_logout=datetime.now())
		user_profile.save()
	logout(request)
	messages.success(request, 'You have successfully logged out!')
	return render(request, 'registration/logout.html')


class PasswordResetView(PasswordResetView):
	template_name = 'registration/psswd_reset_form.html'
	email_template_name='registration/psswd_reset_email.html'


class PasswordResetDoneView(PasswordResetDoneView):
	template_name='registration/psswd_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
	template_name='registration/psswd_reset_confirm.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
	template_name='registration/psswd_reset_complete.html'


@login_required
def home(request):
	""" view function for home page """

	# object count for charts
	num_courses = 2 #Course.objects.all().count()
	return render(
		request,
		'home.html',
		{
			'courses': num_courses,
		}
	)



def register(request):
	"""
		function accepts get and post requests
		GET:  returns forms for registration and user profile creation
		POST:
			- a new user object is created when the form is valid
			- a profile object for the new user is also created
	"""
	# TODO: only invited users should access this function
	try:
		if not request.user.is_authenticated:
			next = request.GET.get('next')
			if request.method == 'POST':
				user_form = UserForm(request.POST)
				profile_form = ProfileForm(request.POST)
				if user_form.is_valid() and profile_form.is_valid():
					user = user_form.save(commit=False)
					profile = profile_form.save(commit=False)
					first_name = user_form.cleaned_data.get('first_name')
					last_name = user_form.cleaned_data.get('last_name')
					password = user_form.cleaned_data.get('password')
					email = user_form.cleaned_data.get('email')
					split_email = email.split('@')
					user.is_active = True
					user.username = split_email[0]
					user.first_name = first_name
					user.last_name =  last_name
					user.email = email
					user.set_password(password)
					user.save()
					profile = Profile(
						user = User.objects.get(pk=user.id),
						bio = profile_form.cleaned_data.get('bio')
					)
					profile.save()
					# NOTE:
					# 	- since users are invited, no need for confirmation email
					#	- uncomment the code below to allow sending account activation emails
					# current_site = get_current_site(request)
					# mail_subject = 'Activate your blog account.'
					# message = render_to_string('registration/acc_activation_email.html',
					# {
					# 	'user': user,
					# 	'domain': current_site.domain,
					# 	'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					# 	'token':account_activation_token.make_token(user),
					# })
					# to_email = user_form.cleaned_data.get('email')
					# email = EmailMessage(mail_subject, message, to=[to_email])
					# email.send()
					# messages.info(request, 'Please confirm your email address to complete the registration')
					messages.info(request, 'please login to proceed')
					return redirect('landing_page')
				else:
					messages.error(request, 'registration failed, please try again')
			user_form = UserForm()
			profile_form = ProfileForm()
			return render(request, 'registration/register.html',
				{'user_form': user_form, 'profile_form': profile_form})
		else:
			messages.info(request, 'You\'re already logged in!')
			return redirect('home')
	except Exception as e:
		print('here\n', e)
		messages.error(request, 'an error occured and registration was not successful')
		return redirect('landing_page')