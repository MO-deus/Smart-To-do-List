"""Enhanced DRF serializers with validation and business logic."""

from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

from .models import Category, Task, ContextEntry


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model with validation and field mapping."""
    
    usage_frequency = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'usage_frequency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'usage_frequency', 'created_at', 'updated_at']
    
    def validate_name(self, value: str) -> str:
        """Validate category name and check for duplicates."""
        if not value or not value.strip():
            raise ValidationError("Category name cannot be empty")
        
        normalized_name = value.strip()
        
        if Category.objects.filter(name__iexact=normalized_name).exists():  # type: ignore
            if self.instance and self.instance.name.lower() == normalized_name.lower():
                return normalized_name
            raise ValidationError("A category with this name already exists")
        
        return normalized_name
    
    def create(self, validated_data: dict) -> Category:
        """Create a new Category instance."""
        return Category.objects.create(**validated_data)  # type: ignore
    
    def update(self, instance: Category, validated_data: dict) -> Category:
        """Update an existing Category instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.full_clean()
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with validation and computed fields."""
    
    category = serializers.UUIDField(source='category.id', read_only=True, allow_null=True)
    categoryName = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_due_soon = serializers.BooleanField(read_only=True)
    days_until_deadline = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'category', 'categoryName', 'category_id',
            'priority', 'deadline', 'status', 'priority_score',
            'createdAt', 'updatedAt', 'is_overdue', 'is_due_soon',
            'days_until_deadline'
        ]
        read_only_fields = [
            'id', 'createdAt', 'updatedAt', 'is_overdue', 'is_due_soon',
            'days_until_deadline'
        ]
    
    def validate_title(self, value: str) -> str:
        """Validate task title is not empty."""
        if not value or not value.strip():
            raise ValidationError("Task title cannot be empty")
        
        return value.strip()
    
    def validate_deadline(self, value: datetime) -> datetime:
        """Validate deadline is not in the past."""
        if value and value < timezone.now():
            raise ValidationError("Deadline cannot be in the past")
        
        return value
    
    def validate_priority(self, value: int) -> int:
        """Validate priority is 1, 2, or 3."""
        if value not in [1, 2, 3]:
            raise ValidationError("Priority must be 1 (High), 2 (Medium), or 3 (Low)")
        
        return value
    
    def validate_status(self, value: str) -> str:
        """Validate status is one of valid choices."""
        valid_statuses = ['Pending', 'In Progress', 'Completed']
        if value not in valid_statuses:
            raise ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        return value
    
    def validate_priority_score(self, value: float) -> float:
        """Validate priority score is between 0.0 and 1.0."""
        if value is not None and not (0.0 <= value <= 1.0):
            raise ValidationError("Priority score must be between 0.0 and 1.0")
        
        return value
    
    def validate(self, attrs: dict) -> dict:
        """Validate task data and resolve category_id to category object."""
        category_id = attrs.get('category_id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)  # type: ignore
                attrs['category'] = category
            except Category.DoesNotExist:  # type: ignore
                raise ValidationError("Invalid category ID")
        
        attrs.pop('category_id', None)
        
        return attrs
    
    def create(self, validated_data: dict) -> Task:
        """Create a new Task instance."""
        return Task.objects.create(**validated_data)  # type: ignore
    
    def update(self, instance: Task, validated_data: dict) -> Task:
        """Update an existing Task instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.full_clean()
        instance.save()
        return instance


class ContextEntrySerializer(serializers.ModelSerializer):
    """Serializer for ContextEntry model with validation and field mapping."""
    
    sourceType = serializers.CharField(source='source_type')
    processedInsights = serializers.CharField(source='processed_insights', required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    has_insights = serializers.BooleanField(read_only=True)
    content_preview = serializers.CharField(read_only=True)
    
    class Meta:
        model = ContextEntry
        fields = [
            'id', 'content', 'sourceType', 'processedInsights',
            'createdAt', 'has_insights', 'content_preview'
        ]
        read_only_fields = ['id', 'createdAt', 'has_insights', 'content_preview']
    
    def validate_content(self, value: str) -> str:
        """Validate content is not empty."""
        if not value or not value.strip():
            raise ValidationError("Content cannot be empty")
        
        return value.strip()
    
    def validate_sourceType(self, value: str) -> str:
        """Validate source type is one of valid choices."""
        valid_source_types = ['WhatsApp', 'Email', 'Note']
        if value not in valid_source_types:
            raise ValidationError(f"Source type must be one of: {', '.join(valid_source_types)}")
        
        return value
    
    def create(self, validated_data: dict) -> ContextEntry:
        """Create a new ContextEntry instance."""
        return ContextEntry.objects.create(**validated_data)  # type: ignore
    
    def update(self, instance: ContextEntry, validated_data: dict) -> ContextEntry:
        """Update an existing ContextEntry instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.full_clean()
        instance.save()
        return instance


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task lists with display labels."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'category_name', 'priority',
            'priority_label', 'deadline', 'status', 'status_label',
            'created_at', 'is_overdue', 'is_due_soon'
        ]
        read_only_fields = ['id', 'created_at', 'is_overdue', 'is_due_soon']


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category lists with popularity score."""
    
    popularity_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'usage_frequency', 'popularity_score']
        read_only_fields = ['id', 'usage_frequency', 'popularity_score']


class ContextEntryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for context entry lists with content preview."""
    
    content_preview = serializers.CharField(read_only=True)
    
    class Meta:
        model = ContextEntry
        fields = ['id', 'content_preview', 'source_type', 'has_insights', 'created_at']
        read_only_fields = ['id', 'has_insights', 'created_at'] 