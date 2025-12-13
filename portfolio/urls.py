from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.PortfolioListView.as_view(), name='list'),
    path('create/', views.portfolio_create, name='create'),
    path('<int:pk>/', views.PortfolioDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.portfolio_update, name='update'),
    path('<int:pk>/delete/', views.PortfolioDeleteView.as_view(), name='delete'),
]
