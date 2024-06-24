from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.create(email='admin')
            user.set_password('12345')
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write('Суперпользователь создан !')
        except IntegrityError:
            self.stdout.write('Суперпользователь с такой почтой уже был создан !')
