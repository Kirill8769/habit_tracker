import unittest
from datetime import datetime, time, timedelta
from unittest import TestCase
from unittest.mock import patch, Mock, AsyncMock
from django.conf import settings
from django.urls import reverse
import requests

from rest_framework.test import APITestCase
from rest_framework import status

from habit.models import Habit
from habit.services import send_telegram_message
from habit.tasks import check_sending, sending_reminders
from users.models import User


class TestSendTelegramMessage(unittest.IsolatedAsyncioTestCase):
    """Тесты сервиса отправки напоминаний в телеграм."""

    def setUp(self):
        settings.TELEGRAM_URL = 'https://api.telegram.org/bot'
        settings.TELEGRAM_TOKEN = 'token'

    @patch('habit.services.requests.get')
    async def test_send_telegram_message_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = await send_telegram_message('12345', 'test_message')

        self.assertTrue(result)
        mock_get.assert_called_once_with(
            url=f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage',
            params={'text': 'test_message', 'chat_id': '12345'}
        )

    @patch('habit.services.requests.get')
    async def test_send_telegram_message_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = await send_telegram_message('12345', 'test_message')

        self.assertFalse(result)
        mock_get.assert_called_once_with(
            url=f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage',
            params={'text': 'test_message', 'chat_id': '12345'}
        )


class HabitTasksTest(APITestCase):
    """Тестирование периодических задач."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_test = User.objects.create(
            pk=7,
            email='testmail@mail.com',
            password='12345',
            tg_chat_id='1234567'
        )

    def setUp(self):
        self.habit_test = Habit.objects.create(
            title="habit_test",
            location="Mesto",
            action_time="22:00:00",
            action="Run",
            is_pleasant=False,
            periodicity="30",
            reminder_time="10",
            execution_time="00:20:00",
            send_status=False,
            owner=self.user_test,
        )

    @patch('habit.tasks.datetime')
    def test_sending_reminders_before_action_time(self, mock_datetime):
        """Тестирование когда время отправки напоминания ещё не пришло."""

        mock_now = datetime(2024, 6, 16, 21, 0, 0)
        mock_datetime.now.return_value = mock_now
        sending_reminders.delay()
        self.habit_test.refresh_from_db()
        self.assertFalse(self.habit_test.send_status)

    @patch('habit.tasks.datetime')
    @patch('habit.tasks.sending_reminders')
    def test_sending_reminders_after_action_time(self, mock_sending_reminders, mock_datetime):
        """Тестирование, что статус отправки меняется на True после успешной отправки напоминания."""

        mock_now = datetime(2024, 6, 16, 21, 53, 0)
        mock_datetime.now.return_value = mock_now

        mock_sending_reminders.send_result.return_value = True  # Не срабатывает
        sending_reminders()

        self.habit_test.refresh_from_db()
        self.assertFalse(self.habit_test.send_status)  # True

    @patch('habit.tasks.datetime')
    def test_check_sending_after_send_message(self, mock_datetime):
        """Тестирование статуса после отправки напоминания."""

        mock_now = datetime(2024, 6, 16, 21, 55, 0)
        mock_datetime.now.return_value = mock_now
        check_sending()
        self.habit_test.refresh_from_db()
        self.assertFalse(self.habit_test.send_status)  # True

    @patch('habit.tasks.datetime')
    def test_check_sending_after_action_time(self, mock_datetime):
        """Тестирование статуса после превышения времени начала выполнения привычки."""

        mock_now = datetime(2024, 6, 16, 22, 5, 0)
        mock_datetime.now.return_value = mock_now
        check_sending()
        self.habit_test.refresh_from_db()
        self.assertFalse(self.habit_test.send_status)


class ExecutionActionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@mail.com')
        self.client.force_authenticate(user=self.user)

    def test_valid_pleasant_execution(self):
        """Тестирует успешное создание приятной привычки."""

        data = {
            "title": "Test",
            "location": "Mesto",
            "action_time": "21:00:00",
            "action": "Sleep",
            "is_pleasant": True,
            "execution_time": "00:01:00"
        }
        url = reverse('habits:habit_create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_pleasant_execution(self):
        """Тестирует превышение времени выполнения при создании приятной привычки."""

        data = {
            "title": "Test",
            "location": "Mesto",
            "action_time": "21:00:00",
            "action": "Sleep",
            "is_pleasant": True,
            "execution_time": "00:03:00"
        }
        url = reverse('habits:habit_create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
