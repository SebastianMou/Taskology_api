# admin.py
from django.contrib import admin
from .models import TaskCategory, Task, SubTask, Profile, Goal
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(TaskCategory)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Profile)
admin.site.register(Goal)
