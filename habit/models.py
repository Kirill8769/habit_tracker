from datetime import timedelta

from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIODICITY_LIST = [
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье'),
        ('30', 'Каждый день'),
    ]
    REMINDER_TIME_LIST = [
        ('60', 'За 1 час'),
        ('30', 'За 30 минут'),
        ('10', 'За 10 минут'),
        ('5', 'За 5 минут'),
        ('0', 'Не напоминать'),
    ]
    title = models.CharField(max_length=64, verbose_name='Название', help_text='Укажите название привычки')
    location = models.CharField(
        max_length=256,
        verbose_name='Место',
        help_text='Укажите место, в котором необходимо выполнять привычку',
    )
    action_time = models.TimeField(
        verbose_name='Время привычки',
        help_text='Укажите время, когда необходимо выполнять привычку',
    )
    action = models.CharField(
        max_length=512,
        verbose_name='Действие',
        help_text='Укажите что нужно делать',
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка',
        help_text='Привычка является приятной ?',
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        limit_choices_to={'is_pleasant': True},
        **NULLABLE,
        verbose_name='Связанная привычка',
        help_text='Свяжите полезную привычку с приятной',
    )
    periodicity = models.CharField(
        max_length=10,
        choices=PERIODICITY_LIST,
        default='30',
        verbose_name='Периодичность',
        help_text='Выберите периодичность выполнения',
    )
    award = models.CharField(
        max_length=256,
        **NULLABLE,
        verbose_name='Вознаграждение',
        help_text='Укажите чем вы хотите себя вознаградить за выполнение привычки',
    )
    execution_time = models.DurationField(
        default=timedelta(minutes=2),
        verbose_name='Время на выполнение',
        help_text='Укажите время, в течение которого Вы будете выполнять привычку'
    )
    reminder_time = models.CharField(
        max_length=5,
        choices=REMINDER_TIME_LIST,
        default='10',
        verbose_name='Напоминание',
        help_text='Выберите время напоминания',
    )
    send_status = models.BooleanField(default=False, verbose_name='Статус отправки')
    is_public = models.BooleanField(
        default=False,
        verbose_name='Опубликовать',
        help_text='Опубликовать привычку ?'
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id', )
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
