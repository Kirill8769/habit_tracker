from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'action_time',
        'is_pleasant',
        'periodicity',
        'execution_time',
        'is_public',
        'owner',
    )
    list_filter = ('is_pleasant', 'periodicity', 'is_public', 'owner', )
