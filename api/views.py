from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from .serializer import TaskCategorySerializer, TaskSerializer, SubTaskSerializer

from .models import TaskCategory, Task, SubTask

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
    tasks = Task.objects.filter(owner=request.user, category=category_id)
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
    data = request.data.copy()  # Make a mutable copy of request data
    data['owner'] = request.user.id  # Set the owner field based on the authenticated user

    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

