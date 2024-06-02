from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('task-list/<str:pk>/', views.task_list, name='task_list'),
    path('task-project-detail/', views.task_list_detail, name='task-project-detail'),
] 