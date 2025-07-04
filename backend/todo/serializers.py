from rest_framework import serializers
from .models import Category, Task, ContextEntry

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # include all fields

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'deadline', 'status', 'createdAt', 'updatedAt', 'priority_score']

# Serializer for ContextEntry model
class ContextEntrySerializer(serializers.ModelSerializer):
    sourceType = serializers.CharField(source='source_type')
    processedInsights = serializers.CharField(source='processed_insights', required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = ContextEntry
        fields = ['id', 'content', 'sourceType', 'processedInsights', 'createdAt'] 