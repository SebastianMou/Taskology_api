from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def task_list(request, pk):
    return render(request, 'tasks/tasks-list.html', {'pk': pk})

def task_list_detail(request):
    return render(request, 'tasks/task_list_detail.html')




