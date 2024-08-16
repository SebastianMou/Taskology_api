from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import TaskCategorySerializer, TaskSerializer, SubTaskSerializer, ProfileSerializer, NotificationsSerializer
from .models import TaskCategory, Task, SubTask, Profile, Notifications
import openai

openai.api_key = settings.OPENAI_API_KEY  # Replace with your actual OpenAI API key

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        ## Task cateogry projects
        'Task Project': '/task-project/',
        'Task Project Detail View': '/task-project-detail/<str:pk>/',
        'Task Project Create': '/task-project-create/',
        'Task Project Update': '/task-project-update/<str:pk>/',
        'Task Project Delete': '/task-project-delete/<str:pk>/',
        ## Main tasks
        'Task List': '/task-list/',
        'Task Detail': '/task-detail/<str:pk>/',
        'Task Create': '/task-create/',
        'Task Update': '/task-update/<str:pk>/',
        'Task Delete': '/task-delete/<str:pk>/',
        'Task Delete All': '/delete-all-tasks-in-category/<int:category_id>/',
        ## Calender
        'Calender': '/calendar/',
        ## Profile
        'Update Profile': '/update-profile/',
        ## Notifications
        'Notification': '/notifications/',
        ## Analysis
        'Analysis': '/task-analysis/<int:category_id>/',
    }
    return Response(api_urls)

## TASK PROJECT CATEGORY C.R.U.D
@api_view(['GET'])
def task_project(request):
    categories = TaskCategory.objects.filter(owner=request.user)
    data = []
    for category in categories:
        tasks = Task.objects.filter(category=category)[:5]
        task_data = TaskSerializer(tasks, many=True).data
        category_data = TaskCategorySerializer(category).data
        category_data['tasks'] = task_data
        data.append(category_data)
    return Response(data)

@api_view(['GET'])
def task_project_detail(request, pk):
    tasks = TaskCategory.objects.get(id=pk)
    serializer = TaskCategorySerializer(tasks, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def task_project_create(request):
    serializer = TaskCategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)

    return Response(serializer.data)

@api_view(['POST'])
def task_project_update(request, pk):
    task = TaskCategory.objects.get(id=pk)
    serializer = TaskCategorySerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def task_project_delete(request, pk):
    try:
        task = TaskCategory.objects.get(id=pk, owner=request.user)
        task.delete()
        return Response({"message": "Item successfully deleted"})
    except TaskCategory.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

## MAIN TASK C.R.U.D 
@api_view(['GET'])
def task_list(request, category_id):
    category = TaskCategory.objects.get(id=category_id, owner=request.user)
    tasks = Task.objects.filter(owner=request.user, category=category_id).order_by('position')
    serializer = TaskSerializer(tasks, many=True)
    category_serializer = TaskCategorySerializer(category)
    return Response({
        'tasks': serializer.data,
        'category': category_serializer.data
    })

@api_view(['GET'])
def task_detail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def task_create(request):
    data = request.data
    owner = request.user
    category = TaskCategory.objects.get(id=data['category'])

    # Get the highest current position in the category and add 1
    max_position = Task.objects.filter(category=category, owner=owner).aggregate(Max('position'))['position__max']
    new_position = (max_position or 0) + 1

    task = Task.objects.create(
        category=category,
        title=data['title'],
        completed=data.get('completed', False),
        completion_date=data.get('completion_date'),
        completion_time=data.get('completion_time'),
        description=data.get('description', ''),
        position=new_position,
        owner=owner
    )

    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def task_update(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)  # Allow partial updates
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def task_delete(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_all_tasks_in_category(request, category_id):
    tasks = Task.objects.filter(category_id=category_id)
    if not tasks.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    tasks.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

## SEARCH BAR
@api_view(['GET'])
def search_tasks(request):
    query = request.GET.get('q', None)
    if query:
        tasks = Task.objects.filter(title__icontains=query, owner=request.user)
        serialized_tasks = TaskSerializer(tasks, many=True)
        return Response(serialized_tasks.data)
    return Response({"message": "No query provided."}, status=400)

@api_view(['GET'])
def search_categories(request):
    query = request.GET.get('q', None)
    if query:
        categories = TaskCategory.objects.filter(name__icontains=query, owner=request.user)
        serialized_categories = TaskCategorySerializer(categories, many=True)
        return Response(serialized_categories.data)
    return Response({"message": "No query provided."}, status=400)

## CALENDER
@api_view(['GET'])
def calendar_events(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

## PROFILE
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## NOTIFICATIONS
@api_view(['GET'])
def notifications(request):
    notifications = Notifications.objects.all()
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def notification_detail(request, pk):
    try:
        notification = Notifications.objects.get(id=pk)
        if not notification.read:
            notification.read = True
            notification.save()
        serializer = NotificationsSerializer(notification, many=False)
        return Response(serializer.data)
    except Notifications.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def unread_notifications_count(request):
    count = Notifications.objects.filter(read=False).count()
    return Response({'unread_count': count})


## EVERYTHING AI
def analyze_task_difficulty(tasks):
    # Prepare a list of tasks to analyze
    task_descriptions = "\n".join(
        f"Task: {task['title']}\nDescription: {task.get('description', 'No description')}\nDue Date: {task.get('due_date', 'No due date')}\n"
        for task in tasks
    )

    # Define messages for the chat-based model
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Productivity Assistant that helps users prioritize and complete their tasks efficiently. "
                "Consider the following criteria when recommending task order: "
                "1. Urgency: Tasks with closer deadlines should be prioritized. "
                "2. Importance: Identify tasks that have significant impact or value. "
                "3. Complexity: Balance complex tasks with easier ones to maintain motivation. "
                "4. Energy Levels: Recommend tasks based on the user's energy and focus patterns. "
                "5. Dependencies: Ensure prerequisite tasks are completed first."
            )
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following tasks and suggest the order in which they should be completed. "
                f"Provide a **short summary** for each task in the suggested order:\n\n{task_descriptions}"
            )
        }
    ]

    # Call the OpenAI API with chat-based completion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=messages,
        max_tokens=250,
        temperature=0.5
    )

    # Extract the response text correctly
    print(task_descriptions)
    print(response.choices[0].message.content.strip())
    analysis = response.choices[0].message.content.strip()
    return analysis

@login_required
def task_analysis(request, category_id):
    # Fetch tasks for the category
    tasks = Task.objects.filter(category_id=category_id, owner=request.user)
    task_list = tasks.values('title', 'description', 'due_date')

    # Analyze task difficulty using OpenAI
    analysis = analyze_task_difficulty(task_list)

    return JsonResponse({'analysis': analysis})

## SORTABLEJS - (https://sortablejs.github.io/Sortable/)
@csrf_exempt
@api_view(['POST'])
def update_task_positions(request):
    data = request.data
    for task_data in data:
        task_id = task_data['id']
        new_position = task_data['position']
        task = Task.objects.get(id=task_id, owner=request.user)
        task.position = new_position
        task.save()
    return Response({'success': True}, status=status.HTTP_200_OK)


