from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all()
