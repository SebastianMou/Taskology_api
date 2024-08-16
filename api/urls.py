from django.urls import path

from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    ## TASK PROJECT CATEGORY C.R.U.D
    path('task-project/', views.task_project, name='task-project'),
    path('task-project-detail/<str:pk>/', views.task_project_detail, name='task-project-detail'),
    path('task-project-create/', views.task_project_create, name='task-project-create'),
    path('task-project-update/<str:pk>/', views.task_project_update, name='task-project-update'),
    path('task-project-delete/<str:pk>/', views.task_project_delete, name='task-project-delete'),
    ## MAIN TASK C.R.U.D
    path('task-list/<int:category_id>/', views.task_list, name='task-list'),
    path('task-detail/<str:pk>/', views.task_detail, name='task-detail'),
    path('task-create/', views.task_create, name='task-create'),
    path('task-update/<str:pk>/', views.task_update, name='task-update'), 
    path('task-delete/<str:pk>/', views.task_delete, name='task-delete'),
    path('delete-all-tasks-in-category/<int:category_id>/', views.delete_all_tasks_in_category, name='delete-all-tasks-in-category'), 
    ## SEARCH BAR
    path('tasks/search/', views.search_tasks, name='search-tasks'),
    path('categories/search/', views.search_categories, name='search-categories'),
    ## CALENDER
    path('calendar/', views.calendar_events, name='calendar-events'),
    ## PROFILE
    path('update-profile/', views.update_profile, name='update-profile'),
    ## NOTIFICATIONS
    path('notifications/', views.notifications, name='notifications'),
    path('notification-detail/<str:pk>/', views.notification_detail, name='notification-detail'),
    path('unread-notifications-count/', views.unread_notifications_count, name='unread-notifications-count'),

    ## EVERYTHING AI
    path('task-analysis/<int:category_id>/', views.task_analysis, name='task-analysis'),
    ## SORTABLEJS
    path('update-task-positions/', views.update_task_positions, name='update-task-positions'),
] 