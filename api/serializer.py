from rest_framework import serializers
from .models import TaskCategory, Task, SubTask

class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'  # Alternatively, list all fields explicitly
        extra_fields = ['category_name', 'category_id']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(TaskSerializer, self).get_field_names(declared_fields, info)
        if hasattr(self.Meta, 'extra_fields'):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
        
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'