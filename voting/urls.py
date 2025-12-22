from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    # Список голосувань
    path('', views.VoteListView.as_view(), name='vote_list'),
    
    # Детальний перегляд та голосування
    path('<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),
    
    # Результати голосування
    path('<int:pk>/results/', views.VoteResultsView.as_view(), name='vote_results'),
    
    # CRUD операції (тільки для модераторів/адміністраторів)
    path('create/', views.VoteCreateView.as_view(), name='vote_create'),
    path('<int:pk>/update/', views.VoteUpdateView.as_view(), name='vote_update'),
    path('<int:pk>/delete/', views.VoteDeleteView.as_view(), name='vote_delete'),
]