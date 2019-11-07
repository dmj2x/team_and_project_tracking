from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Permission, Group
from decouple import config

def create_admin_user():
    '''create default admin user'''
    username = config('ADMIN_USERNAME')
    email = config('ADMIN_EMAIL')
    password = config('ADMIN_PASSWORD')
    try:
        admin_user = User.objects.get(username=username)
    except User.DoesNotExist:
        admin = User.objects.create_superuser(email=email, username=username, password=password)
        admin.is_active = True
        admin.is_staff = True
        admin.save()
        group_name = config('ADMIN_GROUP')
        admin_group = Group.objects.get(name=group_name)
        admin_group.user_set.add(admin)


def create_admin_group():
    ''' create default admin group'''
    group_name = config('ADMIN_GROUP')
    try:
        admin_group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        perms = permissions_list = Permission.objects.all()
        group = Group.objects.create(name=group_name)
        group.save()
        group.permissions.set(perms)


def add_admin_to_group():
    ''' add admin to admin group'''
    group_name = config('ADMIN_GROUP')
    username = config('ADMIN_USERNAME')
    try:
        admin_group = Group.objects.get(name=group_name)
        admin_user = User.objects.get(username=username)
        if not admin_user.groups.filter(name=group_name).exists():
            admin_group.user_set.add(admin_user)
    except Group.DoesNotExist:
        create_admin_group()
        create_admin_user()
        admin_group = Group.objects.get(name=group_name)
        admin_user = User.objects.get(username=username)
        if not admin_user.groups.filter(name=group_name).exists():
            admin_group.user_set.add(admin_user)


class Command(BaseCommand):
    help = 'creates default superuser'
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
        create_admin_group()
        self.stdout.write(self.style.SUCCESS('Success - Admin group created!'))
        create_admin_user()
        self.stdout.write(self.style.SUCCESS('Success - Admin user created!'))
        add_admin_to_group()
        self.stdout.write(self.style.SUCCESS('Success - user added to admin group!'))
