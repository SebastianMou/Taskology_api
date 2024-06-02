from django.urls import path

from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('task-project/', views.task_project, name='task-project'),
    path('task-project-detail/<str:pk>/', views.task_project_detail, name='task-project-detail'),
    path('task-project-create/', views.task_project_create, name='task-project-create'),
    path('task-project-update/<str:pk>/', views.task_project_update, name='task-project-update'),
    path('task-project-delete/<str:pk>/', views.task_project_delete, name='task-project-delete'),
    ## TASK PROJECT CATEGORY C.R.U.D  
    path('task-list/<int:category_id>/', views.task_list, name='task-list'),
    path('task-detail/<str:pk>/', views.task_detail, name='task-detail'),
    path('task-create/', views.task_create, name='task-create'),
    path('task-delete/<str:pk>/', views.task_delete, name='task-delete'),

] 
