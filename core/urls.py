from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Відображення профілю групи (головна сторінка)
    path('', views.GroupProfileView.as_view(), name='group_profile'),
    # Відображення профілю користувача
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    # Оновлення профілю користувача
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='user_profile_edit'),
    # Реєстрація
    path('signup/', views.SignUpView.as_view(), name='signup'),
]