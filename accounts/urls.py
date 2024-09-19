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
    path('dashboardadmin/', views.dashboardadmin, name='dashboardadmin'),
    path('access-denied/', views.access_denied, name='access_denied'),

    path('students/', views.student_list, name='student_list'),
    # path('add_student/', views.add_student, name='add_student'),
    path('create_student/', views.create_student, name='create_student'),
     path('update-student/<int:pk>/', views.update_student, name='update_student'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),
]