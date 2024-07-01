from datetime import timedelta

from rest_framework.exceptions import ValidationError

from habit.models import Habit


class ExecutionActionValidator:
    """
    Проверяет чтобы время выполнения приятной привычки не превышало двух минут,
    а выполнение полезной привычки не превышало полтора часа.
    """

    def __init__(self, execution, is_pleasant):
        self.execution = execution
        self.is_pleasant = is_pleasant

    def __call__(self, value):
        execution_time = dict(value).get(self.execution)
        pleasant_field = dict(value).get(self.is_pleasant)
        if execution_time and pleasant_field:
            if execution_time > timedelta(minutes=2):
                raise ValidationError('Время выполнения приятной привычки должно быть не больше двух минут.')
        if execution_time and not pleasant_field:
            if execution_time > timedelta(minutes=90):
                raise ValidationError('Время выполнения полезной привычки должно быть не больше полутора часов.')


class PeriodicityValidator:
    """Проверяет что если выбран пункт - Каждый день, то другие дни указывать не нужно."""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        pass
        # periodicity_list = dict(value).get(self.periodicity)
        # if len(periodicity_list) > 1 and 'Everyday' in periodicity_list:
        #     raise ValidationError('При указании периода - каждый день, другие дни указывать не нужно.')


class RelatedAwardValidator:
    """
    Проверяет чтобы не было выбрано одновременно связанная полезная привычка и вознаграждение,
    и что бы в список выбора связанных привычек попадали только приятные привычки.
    """

    def __init__(self, related, award):
        self.related = related
        self.award = award

    def __call__(self, values):
        related_field = dict(values).get(self.related)
        award_field = dict(values).get(self.award)
        if related_field and award_field:
            raise ValidationError('Нельзя одновременно указывать связанную полезную привычку и вознаграждение.')
        if related_field:
            pleasant_habit_exists = Habit.objects.filter(is_pleasant=True, pk=related_field.pk).exists()
            if not pleasant_habit_exists:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
                )


class PleasantHabitValidator:
    """Проверяет чтобы при отметке приятная привычка, не были выбраны вознаграждение и связанная приятная привычка."""

    def __init__(self, is_pleasant, award, related):
        self.is_pleasant = is_pleasant
        self.award = award
        self.related = related

    def __call__(self, values):
        pleasant_field = dict(values).get(self.is_pleasant)
        award_field = dict(values).get(self.award)
        related_field = dict(values).get(self.related)
        if pleasant_field and (award_field or related_field):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
