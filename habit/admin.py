from django.contrib import admin
from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'action_time', 'pleasant', 'periodicity', 'execution_time', 'public', 'owner', )
    list_filter = ('pleasant', 'periodicity', 'public', 'owner', )
