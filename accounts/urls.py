from django.urls import path
from . import views
from .views import calculate_score
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
   path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('calculate_score/', calculate_score, name='calculate_score'),
]