from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create default superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        email = 'maiizainelabdeen@gmail.com'
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Default superuser already exists: {email}')
            )
        else:
            User.objects.create_superuser(
                email=email,
                password='Mm22112001*',
                full_name='Mai Zain Elabdeen'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Default superuser created: {email}')
            )
