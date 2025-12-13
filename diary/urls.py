from django.urls import path
from .views import GradeListView, GradeCreateView, GradeUpdateView, GradeDeleteView

urlpatterns = [
    path('', GradeListView.as_view(), name='grade-list'),
    path('add/', GradeCreateView.as_view(), name='grade-add'),
    path('<int:pk>/edit/', GradeUpdateView.as_view(), name='grade-edit'),
    path('<int:pk>/delete/', GradeDeleteView.as_view(), name='grade-delete'),
]



