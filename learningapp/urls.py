from django.contrib import admin
from django.urls import path
from . import views

 
from .views import login,admin_index


from .views import quiz_view, grade_quiz

from .views import submit_quiz


# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('courses/', views.courses, name='courses'),
   
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),

    path('admin_index/', admin_index, name='admin_index'),

    path('view/', views.view, name='view'),

    path('delete/<int:id>/', views.delete, name='delete'),
   
    path('edit/<int:id>/', views.edit, name='edit'),

    path('update/<int:id>/', views.update, name='update'),

    path('course_fullview/', views.course_fullview, name='course_fullview'),

    path('add_to_cart/<int:course_fullview_id>/', views.add_to_cart, name='add_to_cart'),


    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),


    path('admin_quiz/',views.admin_quiz, name='admin_quiz'),

    path('create_question/', views.create_question, name='create_question'),


    path('create_choice/', views.create_choice, name='create_choice'),


    path('quiz/', views.quiz_view, name='quiz_view'),


    path('grade/',views.grade_quiz, name='grade_quiz'),

    path('submit_quiz/', submit_quiz, name='submit_quiz'),


 
]





    




















