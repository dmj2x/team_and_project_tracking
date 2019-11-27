from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Permission, Group
from team_project_tracking.models import *
from decouple import config

def create_roles():
    '''create default roles'''
    try:
        faculty = Role.objects.get_or_create(role_title="Faculty")
        student = Role.objects.get_or_create(role_title="Student")
        teaching_assistant = Role.objects.get_or_create(role_title="Teaching Assistant")
    except Exception as e:
        print('Error occurred in creating default role: %s' % e)


class Command(BaseCommand):
    help = 'creates default roles'
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_const',
            const=False,
            dest='interactive',
            help='do not prompt user inputs',
        )
    def handle(self, **options):
        create_roles()
        self.stdout.write(self.style.SUCCESS('Success - Roles created!'))
