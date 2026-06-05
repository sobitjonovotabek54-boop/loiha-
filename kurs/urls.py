from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='kurs_list'),
    path('course/<int:pk>/', views.course_detail, name='kurs_detail'),
    path('course/add/', views.course_add, name='kurs_add'),
    path('course/<int:pk>/edit/', views.course_edit, name='kurs_edit'),
    path('teacher/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/add/', views.student_add, name='student_add'),
    path('students/', views.student_list, name='student_list'),
]
