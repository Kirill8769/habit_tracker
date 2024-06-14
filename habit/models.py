from datetime import timedelta

from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIODICITY_LIST = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
        ('Everyday', 'Каждый день'),
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
    pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка',
        help_text='Привычка является приятной ?',
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        limit_choices_to={'pleasant_habit': True},
        **NULLABLE,
        verbose_name='Связанная привычка',
        help_text='Свяжите полезную привычку с приятной',
    )
    periodicity = models.CharField(
        max_length=10,
        choices=PERIODICITY_LIST,
        default='Everyday',
        verbose_name='Периодичность',
        help_text='Выберите периодичность выполнения',
    )
    award = models.CharField(
        max_length=256,
        **NULLABLE,
        verbose_name='Вознаграждение',
        help_text='Укажите чем вы хотите себя вознаградить за выполнение привычки',
    )
    execution_time = models.TimeField(
        default=timedelta(minutes=5),
        verbose_name='Время на выполнение',
        help_text='Укажите время, в течение которого Вы будете выполнять привычку'
    )
    public = models.BooleanField(
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
