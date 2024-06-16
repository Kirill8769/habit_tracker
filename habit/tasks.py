import asyncio

from datetime import datetime, timedelta

from celery import shared_task

from habit.models import Habit
from habit.services import send_telegram_message


@shared_task
def sending_reminders():
    """Выполняет отправку напоминаний о необходимости выполнить привычку."""

    habits = Habit.objects.exclude(reminder_time='0').filter(send_status=False)
    for habit in habits:
        tg_chat_id = habit.owner.tg_chat_id
        if tg_chat_id:
            time_now = datetime.now().time()
            weekday = datetime.now().weekday()
            habit_day = int(habit.periodicity)
            if habit_day == 30 or habit_day == weekday:
                habit_time = habit.action_time
                habit_time_delta = timedelta(
                    hours=habit_time.hour,
                    minutes=habit_time.minute,
                    seconds=habit_time.second
                )
                time_now_delta = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
                if time_now_delta > habit_time_delta:
                    continue
                check_time = habit_time_delta - time_now_delta
                reminder_time = int(habit.reminder_time)
                if reminder_time != 0 and check_time <= timedelta(minutes=reminder_time):
                    message = (f'Напоминание\n'
                               f'Привычка: {habit.title}\n'
                               f'Состояние: {"Приятная" if habit.is_pleasant else "Полезная"}\n'
                               f'Что нужно делать: {habit.action}\n'
                               f'Время начала: {habit.action_time}\n'
                               f'Время на выполнение: {habit.execution_time}')
                    send_result = asyncio.run(send_telegram_message(chat_id=habit.owner.tg_chat_id, message=message))
                    if send_result:
                        habit.send_status = True
                        habit.save()


@shared_task
def check_sending():
    """Проверяет было ли отправлено уведомление."""

    habits = Habit.objects.exclude(reminder_time='0').filter(send_status=True)
    for habit in habits:
        habit_time = habit.action_time
        habit_time_delta = timedelta(hours=habit_time.hour, minutes=habit_time.minute, seconds=habit_time.second)
        time_now = datetime.now().time()
        time_now_delta = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
        if time_now_delta > habit_time_delta:
            habit.send_status = False
            habit.save()
