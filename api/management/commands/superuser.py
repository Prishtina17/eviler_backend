from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates a superuser with the default User model."


    def add_arguments(self, parser):
        parser.add_argument(
            '-u', '--username', dest='username', required=True,
            help='The username for the superuser.'
        )
        parser.add_argument(
            '-e', '--email', dest='email', required=True,
            help='The email address for the superuser.'
        )
        parser.add_argument(
            '-p', '--password', dest='password', required=True,
            help='The password for the superuser.'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            raise CommandError(f"Username '{username}' already exists.")

        user = User.objects.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
