from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='user_list'),
    path('create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('detail/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('token/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
