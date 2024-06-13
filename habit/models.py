from datetime import timedelta

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIODICITY_LIST = [
        ('D', 'Раз в день'),
        ('W', 'Раз в неделю'),
        ('M', 'Раз в месяц')
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
    pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка',
        help_text='Привычка является приятной ?',
    )
    periodicity = models.CharField(
        max_length=1,
        choices=PERIODICITY_LIST,
        default='D',
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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id', )
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
