from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a demo superuser for deployment'

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@gmail.com',
                    password='Admin123!',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS('Demo superuser created successfully!')
                )
                self.stdout.write('Username: admin')
                self.stdout.write('Password: Admin123!')
                self.stdout.write('Email: admin@gmail.com')
            else:
                self.stdout.write(
                    self.style.WARNING('Admin user already exists')
                )
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
