from io import StringIO

from django.core.management import call_command
from rest_framework.test import APITestCase

from users.models import User


class CreateSuperuserCommandTest(APITestCase):

    def test_create_superuser(self):
        """Тестирует команду создания суперпользователя."""

        out = StringIO()
        call_command('csu', stdout=out)

        user = User.objects.get(email='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertIn('Суперпользователь создан !', out.getvalue())
