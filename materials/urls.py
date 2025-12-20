from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialDeleteView, MaterialUpdateView

urlpatterns = [
    path('', MaterialListView.as_view(), name='material-list'),
    path('create/', MaterialCreateView.as_view(), name='material-create'),
    path('update/<int:pk>/', MaterialUpdateView.as_view(), name='material-update'),
    path('delete/<int:pk>/', MaterialDeleteView.as_view(), name='material-delete'),
]

app_name = 'materials'