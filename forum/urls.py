from django.urls import path
from .views import ThemesListView, CreateTheme, ThemeDetailView, PostCreationView, ThemeDeletionView, ThemeUpdateView
urlpatterns = [
    path('forum/theme/<int:pk>/', ThemeDetailView.as_view(), name='theme-detail'),
    path('forum/themes/', ThemesListView.as_view(), name='theme-list'),
    path('forum/theme-creation/', CreateTheme.as_view(), name='theme-creation'),
    path('forum/theme/<int:pk>/post-creation/', PostCreationView.as_view(), name='post-creation'),
    path('forum/theme/<int:pk>/theme-deletion/', ThemeDeletionView.as_view(), name='theme-deletion'),
    path('forum/theme/<int:pk>/theme-updation/', ThemeUpdateView.as_view(), name='theme-updation')
]