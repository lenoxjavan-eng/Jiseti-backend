import os

from django.core.management.base import BaseCommand, CommandError

from apps.users.models import User


class Command(BaseCommand):
    help = 'Create or update the configured deployment administrator.'

    def handle(self, *args, **options):
        email = os.getenv('ADMIN_EMAIL', '').strip().lower()
        password = os.getenv('ADMIN_PASSWORD', '')

        if not email or not password:
            self.stdout.write('ADMIN_EMAIL and ADMIN_PASSWORD are not configured; skipping admin bootstrap.')
            return

        user, created = User.objects.get_or_create(email=email)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(update_fields=('password', 'is_active', 'is_staff', 'is_superuser'))

        action = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Deployment administrator {action}: {email}'))
