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
from django.shortcuts import render, redirect, get_object_or_404
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
			return redirect('user_profile')
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
	return render(request,'home.html')



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


@login_required
def get_user_role(request):
	user_role = ''
	current_user = User.objects.get(pk=request.user.id)
	check_fac_role = current_user.faculty.values().count()
	check_stu_role = current_user.student.values().count()
	if check_fac_role > 0 and check_stu_role < 1:
		user_role = 'Faculty'
	elif check_fac_role < 1 and check_stu_role > 0:
		user_role = 'Student'
	return user_role



@login_required
def user_profile(request):
	"""
		function accepts get requests only
		GET: returns current user's profile information
	"""
	user_role = get_user_role(request)
	obj, created = Profile.objects.update_or_create(user=request.user, user_role=user_role.title())
	if created==1:
		logging.debug("user role updated")
	else:
		logging.debug("user role not updated")
	try:
		user_info = User.objects.get(pk=request.user.id)
		return render(request, 'team_project_tracking/user_profile.html', {'user_info': user_info, 'user_role':user_role} )
	except Exception as e:
		logger.debug("an error occurred trying to view a user profile")
		messages.error(request,
			'an error occurred trying to view a user profile. The Site Administrator will be notified!')
		return redirect('home')


# @login_required
# def change_password(request):
# 	"""
# 		function accepts get and post requests
# 		GET:  returns a password change form
# 		POST:
# 			- user password is updated
# 			- user is redirected to login page to be reauthenticated
# 	"""
# 	if request.method == 'POST':
# 		password_form = PasswordChangeForm(request.user, request.POST)
# 		try:
# 			if password_form.is_valid():
# 				user = password_form.save()
# 				update_session_auth_hash(request, user)
# 				messages.success(request, 'Your password was successfully updated!')
# 				return redirect(reverse('login') + '?next=/medwater/user_profile/')
# 			else:
# 				logger.warning("password change failed")
# 				messages.error(request, 'Password change failed! Make sure the old password is correct!')
# 		except ObjectDoesNotExist:
# 			logger.error("error occured when a user tried to make a password change")
# 			messages.error(request,
# 				'an error occured truing to change your password. The site administrator will be notified!')
# 		return redirect('user_profile')
# 	else:
# 		password_form = PasswordChangeForm(request.user)
# 		return render(request, 'medwater/change_password.html', {'password_form': password_form})




@login_required
# TODO: check permissions and roles
def roles_list(request):
	try:
		roles = Role.objects.all()
		return render(request, 'team_project_tracking/roles_list.html', {'roles':roles})
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to view roles list!')
		return redirect('home')


@login_required
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
	try:
		if request.user.is_superuser:
			if request.method == 'POST':
				form = UserRoleForm(request.POST)
				if form.is_valid():
					course_offering = form.cleaned_data.get('course_offering') 
					user = form.cleaned_data.get('user')
					role = form.cleaned_data.get('role')
					print('USer: %s' % user.first_name)
					new_user_role = UserRole(
						role=role,
						course_offering=course_offering,
						user=user
						)
					new_user_role.save()
					messages.success(request, 'role assigned successfully!')
					return redirect('home')
				else:
					messages.warning(request, 'role was not assigned')
					# return redirect('home')
					return render(request, 'team_project_tracking/assign_role_form.html', {'form': form})
			else:
				form = UserRoleForm()
				return render(request, 'team_project_tracking/assign_role_form.html', {'form': form})
		else:
			messages.warning(request, 'you don\'t have permission to aassign roles!')
			return redirect('home')
	except Exception as e:
		logging.debug(e)


@login_required
def unassign_role(request):
	if request.method == 'POST':
		form = UserRoleForm(request.POST)
		course_offering = form.data['course_offering']
		user = form.data['user']
		role = form.data['role']
		try:
			remove_user_role = UserRole.objects.filter(
				role=role,
				course_offering=course_offering,
				user=user).first()
			if(remove_user_role):
				remove_user_role.delete()
				messages.success(request, 'user role removed successfully!')
				return redirect('home')
			else:
				check_course_offering = CourseOffering.objects.get(pk=course_offering)
				check_user = User.objects.get(pk=user)
				check_role = Role.objects.get(pk=role)
				messages.warning(request, "There is no user called %s with role %s in  %s course!" % (
					check_user.first_name, check_role.role_title, check_course_offering))
				return redirect('home')
		except Exception as e:
			logging.debug(e)
			# TODO: re-route to appropriate page
			messages.error(request, "an error occurred trying to unassign a role")
			return redirect('home')
	else:
		form = UserRoleForm()
	return render(request, 'team_project_tracking/unassign_role_form.html', {'form': form})


@login_required
# TODO: check permissions and roles
def course_list(request):
	try:
		courses = Course.objects.all()
		return render(request, 'team_project_tracking/course_list.html', {'courses':courses})
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to view course list!')
		return redirect('home')


@login_required
# should require system admin
def add_course(request):
	if request.user.is_superuser:
		try:
			if request.method == 'POST':
				course_form = CourseForm(request.POST)
				if course_form.is_valid():
					course_name = course_form.cleaned_data.get('course_name')
					course_number = course_form.cleaned_data.get('course_number')
					course_description = course_form.cleaned_data.get('course_description')
					faculty = course_form.cleaned_data.get('faculty')
					
					num_results = Course.objects.filter(course_name=course_name.title(), course_number=course_number, faculty=faculty).count()
					# TODO: or we can use course_name__contains in the filter when the above query fails to return the desire results
					if num_results < 1:
						course = Course(
							course_name=course_name.title(),
							course_number=course_number,
							course_description=course_description,
							faculty=faculty
						)
						course.save()
						# assign faculty role to registered faculty
						faculty_role = Role.objects.get(role_title='Faculty')
						assign_role, created = UserRole.objects.get_or_create(
							role=faculty_role,
							user=faculty
						)
						print('created: %s' % created)
						messages.success(request, 'Course successfully added!')
					else:
						messages.info(request, 'a course with name %s already exists!' % course_name)
					return redirect('course_list')
				else:
					return render(request, 'team_project_tracking/add_course_form.html', {'form': course_form})
			else:
				course_form = CourseForm()
				return render(request, 'team_project_tracking/add_course_form.html', {'form': course_form})
		# except Exception as e:
		except PermissionDenied:
			messages.error(request, 'an error occurred, please contact site administrator!')
			# TODO: this will redirect to a custom 404 page
			return redirect('home')
	else:
		messages.warning(request, 'you don\'t have the required permission to add a new course')
		return redirect('home')


@login_required
def add_course_offering(request, pk):
	user_role = get_user_role(request)
	if pk and user_role=='Faculty':
		course = Course.objects.get(pk=pk)
		if request.user == course.faculty or request.user.is_superuser:
			try:
				if request.method == 'POST':
					course_offering_form = CourseOfferingForm(request.POST)
					if course_offering_form.is_valid():
						semester = course_offering_form.cleaned_data.get('semester')
						year = course_offering_form.cleaned_data.get('year')
						
						num_results = CourseOffering.objects.filter(course=course, semester=semester, year=year).count()
						# TODO: or we can use course_name__contains in the filter when the above query fails to return the desire results
						if num_results < 1:
							course_offer = CourseOffering(
								course = course,
								semester=semester,
								year=year
							)
							course_offer.save()
							messages.success(request, 'Course offering successfully added!')
						else:
							messages.info(request, 'a course offering for %s,  %s%s already exists!' % (course.course_name, semester, year))
						return redirect('course_details', pk)
					else:
						return render(request, 'team_project_tracking/add_course_offering_form.html', {'form': course_offering_form})
				else:
					course_offering_form = CourseOfferingForm()
					return render(request, 'team_project_tracking/add_course_offering_form.html', {'form': course_offering_form, "course_id":pk})
			except Exception as e:

				messages.error(request, 'an error occurred, please contact site administrator!')
				return redirect('home')
		else:
			messages.warning(request, 'you don\'t have the required permission to add a new course')
			return redirect('home')
	else:
		messages.warning(request, 'an error occurred, please contact site administrator!')
		return redirect('home')


@login_required
def course_details(request, pk):
	user_role = get_user_role(request)
	try:
		if (pk):
			course = Course.objects.get(pk=pk)
			course_offering, current_offering, course_teams, current_students = [], [], [], []
			try:
				current_offering = CourseOffering.objects.filter(course=course).last()
				if current_offering:
					course_offering = CourseOffering.objects.filter(course=course).order_by('year').exclude(id=current_offering.id)
					course_teams = Team.objects.filter(course_offering=current_offering)
					current_students = CourseStudent.objects.filter(course_offering=current_offering).exclude(student_role="teaching-assistant", student_status='declined')
					
			except Exception as e:
				logger.debug(e)
				# print("Course is missing more info")
			return render(request, 
				'team_project_tracking/course_detail.html', 
				{
					'course' : course,
					'user_role' : user_role,
					'course_offering' : course_offering,
					'current_offering' : current_offering,
					'course_teams' : course_teams,
					'current_students' : current_students
				}
			)
	except Course.DoesNotExist:
		messages.error(request, 'an error occurred trying to view course details!')
		# TODO: this will redirect to a custom 404 page
		return redirect('home')


@login_required
def edit_course_info(request, pk):
	try:
		if (pk):
			course = Course.objects.get(pk=pk)
			form = CourseForm(request.POST, instance=course)
			if request.method == 'POST' and form.is_valid():
				# print("here now: %s" % course.course_name)
				course_update = form.save(commit=False)
				course_update.course_name = form.cleaned_data['course_name']
				course_update.course_number = form.cleaned_data['course_number']
				course_update.course_description = form.cleaned_data['course_description']

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



@login_required
def join_course(request):
	if not request.user.faculty.values(): # or request.user.profile.user_role=="Student"
		try:
			if request.method == 'POST':
				join_course_form = JoinCourseForm(request.POST)
				if join_course_form.is_valid():
					course_offering = join_course_form.cleaned_data.get('course_offering')
					num_results = CourseOffering.objects.get(pk=course_offering.id)
					if num_results:
						course_student = CourseStudent(
							course_offering = course_offering,
							student = request.user
						)
						course_student.save()
						messages.success(request, 'Your request to join %s has been made' % course_offering)
						return redirect('user_profile')
					else:
						messages.warning(request, 'The selected course offering does not exist. Please make sure to check all fields!')
						return render(request, 'team_project_tracking/join_course_form.html', {'form': join_course_form})
				else:
					messages.error(request, 'Please make sure to check all fields!')
					return render(request, 'team_project_tracking/join_course_form.html', {'form': join_course_form})
			else:
				join_course_form = JoinCourseForm()
				return render(request, 'team_project_tracking/join_course_form.html', {'form': join_course_form})
		except Exception as e:
			messages.error(request, 'an error occurred, please contact site administrator!')
			return redirect('home')
	else:
		messages.warning(request, 'You don\'t have the right access to perform that action!')
		return redirect('home')


@login_required
def approve_student(request, course_id, course_stu_id):
	try:
		course = Course.objects.get(pk=course_id)
		if course.faculty == request.user:
			update_course_stu = CourseStudent.objects.filter(pk=course_stu_id).update(student_status='approved')
			if update_course_stu==1:
				messages.success(request, 'Student Approved')
			else:
				messages.error(request, 'Oops! Student status was not updated')
			return redirect('course_details', course_id)
		else:
			messages.error(request, 'You don\'t have permission to perform that action!')
			return redirect('home')
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred, please contact site administrator!')
		return redirect('home')



@login_required
def decline_student(request, course_id, course_stu_id):
	try:
		course = Course.objects.get(pk=course_id)
		if course.faculty == request.user:
			update_course_stu = CourseStudent.objects.filter(pk=course_stu_id).update(student_status='decined')
			if update_course_stu==1:
				messages.success(request, 'Student Request Declined')
			else:
				messages.error(request, 'Oops! Student status was not updated')
			return redirect('course_details', course_id)
		else:
			messages.error(request, 'You don\'t have permission to perform that action!')
			return redirect('home')
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred, please contact site administrator!')
		return redirect('home')



@login_required
# TODO: check permissions and roles
def teams_list(request):
	try:
		teams = Team.objects.all()
		return render(request, 'team_project_tracking/teams_list.html', {'teams':teams})
	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to view course list!')
		return redirect('home')


@login_required
# TODO: must be a student or faculty of a given class
def create_new_team(request):
	# should require system admin and faculty roles
	# user should be faculty or student
	if request.user.is_superuser:
		try:
			if request.method == 'POST':
				form = CreateTeamForm(request.POST)
				if form.is_valid():
					team_name = form.cleaned_data.get('team_name')
					course_offering = form.cleaned_data.get('course_offering')
					team_creator = request.user
					if_team = Team.objects.filter(team_name=team_name.title(), course_offering=course_offering, team_creator=team_creator).count()
					# TODO: or we can use course_name__contains in the filter when the above query fails to return the desire results
					if if_team < 1:
						new_team = Team()
						new_team.team_name=team_name.title()
						new_team.course_offering=course_offering
						new_team.team_creator=team_creator
						try:
							role = Role.objects.get(role_title="Faculty")
							check_user_role = UserRole.objects.get(role=role, user=request.user)
							new_team.team_status='active'
						except Exception as e:
							logger.error(e)
							new_team.team_status='pending'
						new_team.save()
						messages.success(request, 'Team successfully created!')
					else:
						# similar_teams = Team.objects.filter(team_name=team_name.title(), course_offering=course_offering, team_creator=team_creator)
						# for team in similar_teams:
						# 	print('Here in teams with: %s' % team)
						messages.info(request, 'a team with name %s already exists!' % team_name)
					return redirect('teams_list')
				else:
					return render(request, 'team_project_tracking/create_team_form.html', {'form': form})
			else:
				form = CreateTeamForm()
				return render(request, 'team_project_tracking/create_team_form.html', {'form': form})
		# except Exception as e:
		except PermissionDenied:
			messages.error(request, 'an error occurred, please contact site administrator!')
			# TODO: this will redirect to a custom 404 page
			return redirect('home')
	else:
		messages.warning(request, 'you don\'t have the required permission to add a new course')
		return redirect('home')


@login_required
def team_details(request, pk):
	try:
		if (pk):
			team = Team.objects.get(pk=pk)
	except Team.DoesNotExist:
		messages.error(request, 'an error occurred trying to view team details!')
		# TODO: this will redirect to a custom 404 page
		return redirect('home')
	return render(request, 'team_project_tracking/team_details.html', {'team' : team})


@login_required
def edit_team_info(request, pk):
	try:
		if (pk):
			team = get_object_or_404(Team, pk=pk)
			form = UpdateTeamInfoForm(request.POST, instance=team)
			if request.method=='POST' and form.is_valid(): # and request.user is student
				team_update = form.save(commit=False)
				team_update.team_name = form.cleaned_data['team_name']
				team_update.course_offering = form.cleaned_data['course_offering']
				
				team_update.save()
				messages.success(request, 'team successfully information updated!')
				return redirect(team_update.get_absolute_url())
			else:
				form = UpdateTeamInfoForm(instance=team)
				return render(request, 'team_project_tracking/edit_team_info.html', {'form': form})

	except Exception as e:
		logger.debug(e)
		messages.error(request, 'an error occurred trying to edit team information!')
		# TODO: this will redirect to the appropriate page
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