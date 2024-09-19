from django.core.management.base import BaseCommand
from accounts.models import CustomUser # Assure-toi que 'account' correspond bien à ton application
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a default admin user if not exists'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create(
                username='admin1@gmail.com',
                password=make_password('test12345'),  # Remplace par le mot de passe souhaité
                is_superuser=True,
                is_staff=True,
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
