from django.urls import path

from habit import views
from habit.apps import HabitConfig

app_name = HabitConfig.name

urlpatterns = [
    path('', views.HabitListAPIView.as_view(), name='habit_list'),
    path('published/', views.HabitPublishedListAPIView.as_view(), name='habit_published_list'),
    path('create/', views.HabitCreateAPIView.as_view(), name='habit_create'),
    path('detail/<int:pk>/', views.HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', views.HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', views.HabitDestroyAPIView.as_view(), name='habit_delete'),
]
