from django.test import TestCase
from django.contrib.auth import get_user_model
from team_project_tracking.models import *
from team_project_tracking.forms import *

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(self):

#         class UserLoginForm(forms.Form):
#             error_css_class = 'error'
#             required_css_class = 'required'
#             username = forms.CharField(label='', widget=forms.TextInput(
#                 attrs={
#                     'class': 'form-control mt-5',
#                     'autofocus': '',
#                     'style': 'width:66ch',
#                     'placeholder': 'Enter username...',
#                 }
#             ), )

#     def setUp(self):
#         user = get_user_model().objects.create_user('system_admin')
#         self.entry = Entry.objects.create(author=user, title="My entry title")
