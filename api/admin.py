from django.contrib import admin
from .models import TaskCategory, Task, SubTask

# Register your models here.
admin.site.register(TaskCategory)
admin.site.register(Task)
admin.site.register(SubTask)