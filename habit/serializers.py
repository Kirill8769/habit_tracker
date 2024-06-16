from rest_framework import serializers

from habit.models import Habit
from habit.validators import ExecutionActionValidator, PleasantHabitValidator, RelatedAwardValidator


class HabitSerializer(serializers.ModelSerializer):
    # periodicity = serializers.MultipleChoiceField(
    #     choices=Habit.PERIODICITY_LIST,
    #     required=False,
    # )

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            ExecutionActionValidator(execution='execution_time', is_pleasant='is_pleasant'),
            RelatedAwardValidator(related='related_habit', award='award'),
            PleasantHabitValidator(related='related_habit', award='award', is_pleasant='is_pleasant'),
        ]
