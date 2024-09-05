from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
   path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]