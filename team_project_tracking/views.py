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
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

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
		logout(request)
		messages.success(request, 'You have successfully logged out!')
	except Exception as e:
		logging.debug(e)
		logger.error('an error occured trying to access admin users')
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
				if user_form.is_valid():
					user = user_form.save(commit=False)
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
						user = User.objects.get(pk=user.id)
					)
					profile.save()
					messages.info(request, 'please login to proceed')
					return redirect('landing_page')
				else:
					messages.error(request, 'registration failed, please try again')
			user_form = UserForm()
			# profile_form = ProfileForm()
			return render(request, 'registration/register.html',
				{'user_form': user_form})
		else:
			messages.info(request, 'You\'re already logged in!')
			return redirect('home')
	except Exception as e:
		logging.debug('A debug message!')
		messages.error(request, 'an error occured and registration was not successful')
		return redirect('landing_page')


def add_user_role(request):
	if request.method == 'POST':
		form = RoleForm(request.POST)
		if form.is_valid():
			role_title = form.cleaned_data.get('role_title')
			description = form.cleaned_data.get('description')

			new_role = Role(
				role_title=role_title,
				description=description)
			new_role.save()
			messages.success(request, 'role added successfully!')
			# TODO: will be routing to an appropriate page
			return redirect('home')
	else:
		form = RoleForm()
	return render(request, 'team_project_tracking/add_role_form.html', {'form': form})


@login_required
def edit_user_role(request, pk):
	try:
		if (pk):
			role = Role.objects.get(pk=pk)
			form = RoleForm(request.POST, instance=role)
			if request.method == 'POST' and form.is_valid():
				role_update = form.save(commit=False)
				role_update.role_title = form.cleaned_data['role_title']
				role_update.description = form.cleaned_data['description']
				role_update.save()
				messages.success(request, 'role information updated!')
				# return redirect(comm_update.get_absolute_url())
				# TODO: will be routing to admin page or page with list of roles
				return redirect('home')
			else:
				form = RoleForm(instance=role)
				return render(request, 'team_project_tracking/edit_role_form.html', {'form': form})

	except Exception as e:
		logging.debug(e)
		messages.error(request, 'an error occurred, please contact site administrator!')
		# TODO: this will redirect to a custom 404 page
		return redirect('home')


@login_required
def assign_role(request):
	if request.method == 'POST':
		form = UserRoleForm(request.POST)
		if form.is_valid():
			course = form.cleaned_data.get('course')
			user = form.cleaned_data.get('user')
			role = form.cleaned_data.get('role')
			new_user_role = UserRole(
				role=role,
				course=course,
				user=user
				)
			new_user_role.save()
			messages.success(request, 'role assigned successfully!')
			# TODO: will be routing to admin page to view members with roles
		return redirect('home')
	else:
		form = UserRoleForm()
	return render(request, 'team_project_tracking/assign_role_form.html', {'form': form})


@login_required
def unassign_role(request):
	if request.method == 'POST':
		form = UserRoleForm(request.POST)
		course = form.data['course']
		user = form.data['user']
		role = form.data['role']
		try:
			remove_user_role = UserRole.objects.filter(
				role=role,
				course=course,
				user=user).first()
			if(remove_user_role.delete()):
				messages.success(request, 'user role removed successfully!')
				return redirect('home')
		except Exception as e:
			logging.debug(e)
			# TODO: re-route to appropriate page
			check_course = Course.objects.get(pk=course)
			check_user = User.objects.get(pk=user)
			check_role = Role.objects.get(pk=role)
			messages.warning(request, "%s has no user, %s with role as %s!" % (
				check_course.course_name, check_user.first_name, check_role.role))
			return redirect('home')
	else:
		form = UserRoleForm()
	return render(request, 'team_project_tracking/unassign_role_form.html', {'form': form})



@login_required
# TODO: check permissions and roles
def course_list(request):
	try:
		courses = Course.objects.all()
		# courseList = []
		# if courses:
		# 	for course in courses:
		# 		courseList.append(course)
		return render(request, 'team_project_tracking/course_list.html', {'courses':courses})
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to view course list!')
		return redirect('home')


@login_required
# should require system admin and faculty roles
def add_course(request):
	# if  request.user.has_perm('medwater.add_community'):
	if request.user.is_superuser:
		try:
			if request.method == 'POST':
				form = CourseForm(request.POST)
				if form.is_valid():
					course_name = form.cleaned_data.get('course_name')
					course_number = form.cleaned_data.get('course_number')
					course_description = form.cleaned_data.get('course_description')
					semester = form.cleaned_data.get('semester')
					year = form.cleaned_data.get('year')
					num_results = Course.objects.filter(course_name=course_name.title()).count()
					# TODO: or we can use course_name__contains in the filter when the above query fails to return the desire results
					if num_results < 1:
						course = Course(
							course_name=course_name.title(),
							course_number=course_number,
							course_description=course_description,
							semester=semester,
							year=year
						)
						course.save()
						messages.success(request, 'Course successfully added!')
					else:
						messages.info(request, 'a course with name %s already exists!' % course_name)
					# TODO: should redirect to course list
					return redirect('home')
				else:
					return render(request, 'team_project_tracking/add_course_form.html', {'form': form})
			else:
				form = CourseForm()
				return render(request, 'team_project_tracking/add_course_form.html', {'form': form})
		# except Exception as e:
		except PermissionDenied:
			messages.error(request, 'an error occurred, please contact site administrator!')
			# TODO: this will redirect to a custom 404 page
			return redirect('home')
	else:
		messages.warning(request, 'you don\'t have the required permission to add a new course')
		return redirect('home')


@login_required
def course_details(request, pk):
	try:
		if (pk):
			course = Course.objects.get(pk=pk)
	except Course.DoesNotExist:
		messages.error(request, 'an error occurred trying to view course details!')
		# TODO: this will redirect to a custom 404 page
		return redirect('home')
	return render(request, 'team_project_tracking/course_detail.html', {'course' : course})


@login_required
def edit_course_info(request, pk):
	try:
		if (pk):
			course = Course.objects.get(pk=pk)
			form = CourseForm(request.POST, instance=course)
			if request.method == 'POST' and form.is_valid():
				print("here now", course.course_name)
				course_update = form.save(commit=False)

				course_update.course_name = form.cleaned_data['course_name']
				course_update.course_number = form.cleaned_data['course_number']
				course_update.course_description = form.cleaned_data['course_description']
				course_update.semester = form.cleaned_data['semester']
				course_update.year = form.cleaned_data['year']

				course_update.save()
				messages.success(request, 'course information updated!')
				return redirect(course_update.get_absolute_url())
			else:
				form = CourseForm(instance=course)
				return render(request, 'team_project_tracking/edit_course_info.html', {'form': form})

	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to edit course information!')
		# TODO: this will redirect to a custom 404 page
		return redirect('home')

# @login_required
# def all_admin_users(request):
# 	""" function returns list of all users in the admin group """
# 	try:
# 		return Group.objects.get(name=config('ADMIN_GROUP')).user_set.all()
# 	except Exception:
# 		logger.error('an error occured trying to access admin users')
# 		messages.error('an error occured and the site administrator will be notified!')
# 		return redirect('home')


# @login_required
# def grant_permission(request):
# 	"""
# 		function accepts get and post requests
# 		GET: returns a form with users and permisions
# 		POST: selected users are assigned the selected permisions
# 	"""
# 	admin_users = all_admin_users(request)
# 	if  request.user.is_staff or request.user in admin_users:
# 		try:
# 			if request.method == 'POST':
# 				# get the list of user ids as string elements
# 				user_select = request.POST.getlist('user-select[]')
# 				# convert the id to integers
# 				user_ids = list(map(int, user_select))
# 				perm_select = request.POST.getlist('perm-select[]')
# 				perm_ids = list(map(int, perm_select))
# 				try:
# 					for u_id in user_ids:
# 						user = User.objects.get(pk=u_id)
# 						for perm_id in perm_ids:
# 							perm = Permission.objects.get(pk=perm_id)
# 							if not user.has_perm(perm):
# 								user.user_permissions.add(perm)
# 					messages.success(request, "permissions successfully added!")
# 				except Exception as e:
# 					logger.warning("granting permissions failed")
# 					messages.error(request, "granting permissions was not successful!")
# 				return redirect('home')
# 			else:
# 				usr_choices = [(usr.pk, usr.first_name) for usr in User.objects.filter(is_active=True, is_staff=False)]
# 				perm_choices = [(perm.pk, perm.name) for perm in Permission.objects.filter(
# 					Q(name__contains='Can add community') |
# 					Q(name__contains='Can add project') |
# 					Q(name__contains='Can add funding') |
# 					Q(name__contains='Can add member'))]
# 				return render(request, 'medwater/add_permission.html',
# 					{'usr_choices': usr_choices, 'perm_choices': perm_choices})
# 		except Exception:
# 			logger.error("an error occurred and permissions cannot be added")
# 			messages.error(request,
# 				'an error occurred and permissions cannot be added. The site Administrator has been notified!')
# 	messages.warning(request, 'you don\'t have permission to access that page!')
# 	return redirect('home')