from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='gallery_list'), 
    path('add/', views.GalleryCreateView.as_view(), name='add_file'), 
    path('register/', views.register_view, name='register'), 
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
]