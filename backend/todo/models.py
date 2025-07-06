# type: ignore[reportAttributeAccessIssue,reportGeneralTypeIssues]
"""Enhanced Django models with validation and business logic."""

import uuid
from datetime import datetime, timedelta
from typing import Optional, cast
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Task categories with usage tracking for intelligent suggestions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Category name (must be unique)"
    )
    usage_frequency = models.IntegerField(
        default=0,  # type: ignore
        validators=[MinValueValidator(0)],
        help_text="Number of times this category has been used"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-usage_frequency', 'name']
        db_table = 'todo_categories'
    
    def __str__(self) -> str:
        return str(self.name)
    
    def clean(self):
        super().clean()
        if self.name:
            name = str(self.name).strip()
            if not name:
                raise ValidationError("Category name cannot be empty")
    
    def increment_usage(self) -> None:
        """Increment usage frequency when task is assigned to this category."""
        self.usage_frequency = int(self.usage_frequency or 0) + 1  # type: ignore
        self.save(update_fields=['usage_frequency', 'updated_at'])
    
    def get_popularity_score(self) -> float:
        """Calculate popularity score (0.0 to 1.0) based on usage frequency."""
        if self.usage_frequency == 0:
            return 0.0
        elif self.usage_frequency <= 5:
            return 0.2
        elif self.usage_frequency <= 10:
            return 0.4
        elif self.usage_frequency <= 20:
            return 0.6
        elif self.usage_frequency <= 50:
            return 0.8
        else:
            return 1.0
    
    @classmethod
    def get_most_popular(cls, limit: int = 10) -> models.QuerySet:
        """Get most popular categories ordered by usage frequency."""
        return cls.objects.order_by('-usage_frequency')[:limit]  # type: ignore
    
    @classmethod
    def get_unused_categories(cls, days: int = 30) -> models.QuerySet:
        """Get categories unused for specified number of days."""
        cutoff_date = timezone.now() - timedelta(days=days)
        return cls.objects.filter(
            usage_frequency=0,
            updated_at__lt=cutoff_date
        )  # type: ignore


class Task(models.Model):
    """Task model with priority, status, deadlines, and AI insights."""
    
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=200,
        help_text="Task title"
    )
    description = models.TextField(
        blank=True,
        help_text="Task description"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Associated category"
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,  # type: ignore
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="Task priority level"
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Task deadline"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        help_text="Current task status"
    )
    priority_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="AI-computed priority score (0.0 to 1.0)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']
        db_table = 'todo_tasks'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['deadline']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return str(self.title)
    
    def clean(self):
        super().clean()
        
        if self.title:
            title = str(self.title).strip()
            if not title:
                raise ValidationError("Task title cannot be empty")
        
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past")
        
        if self.priority_score is not None:
            if not 0.0 <= self.priority_score <= 1.0:
                raise ValidationError("Priority score must be between 0.0 and 1.0")
    
    def save(self, *args, **kwargs):
        """Update category usage frequency when category changes."""
        if self.pk:
            try:
                old_instance = Task.objects.get(pk=self.pk)  # type: ignore
                if old_instance.category != self.category:
                    if old_instance.category:
                        old_instance.category.usage_frequency = int(old_instance.category.usage_frequency or 0) - 1  # type: ignore
                        old_instance.category.save(update_fields=['usage_frequency'])
                    if self.category is not None:
                        cat = cast(Category, self.category)
                        cat.increment_usage()  # type: ignore
            except Exception:
                if self.category is not None:
                    cat = cast(Category, self.category)
                    cat.increment_usage()  # type: ignore
        else:
            if self.category is not None:
                cat = cast(Category, self.category)
                cat.increment_usage()  # type: ignore
        
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is past deadline and not completed."""
        if not self.deadline or self.status == 'Completed':
            return False
        return timezone.now() > self.deadline
    
    @property
    def is_due_soon(self) -> bool:
        """Check if task is due within 7 days and not completed."""
        if not self.deadline or self.status == 'Completed':
            return False
        return timezone.now() <= self.deadline <= timezone.now() + timedelta(days=7)
    
    @property
    def days_until_deadline(self) -> Optional[int]:
        """Calculate days until deadline, returns None if no deadline."""
        if not self.deadline:
            return None
        
        delta = self.deadline - timezone.now()
        return delta.days
    
    def mark_completed(self) -> None:
        self.status = 'Completed'
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_in_progress(self) -> None:
        self.status = 'In Progress'
        self.save(update_fields=['status', 'updated_at'])
    
    def update_priority(self, new_priority: int) -> None:
        """Update task priority (1, 2, or 3)."""
        if new_priority not in [1, 2, 3]:
            raise ValidationError("Priority must be 1, 2, or 3")
        
        self.priority = new_priority
        self.save(update_fields=['priority', 'updated_at'])
    
    def assign_category(self, category: Category) -> None:
        """Assign category to task."""
        self.category = category
        self.save(update_fields=['category', 'updated_at'])
    
    @classmethod
    def get_overdue_tasks(cls) -> models.QuerySet:
        """Get all overdue tasks."""
        return cls.objects.filter(
            deadline__lt=timezone.now(),
            status__in=['Pending', 'In Progress']
        )  # type: ignore
    
    @classmethod
    def get_due_soon_tasks(cls, days: int = 7) -> models.QuerySet:
        """Get tasks due within specified days."""
        future_date = timezone.now() + timedelta(days=days)
        return cls.objects.filter(
            deadline__gte=timezone.now(),
            deadline__lte=future_date,
            status__in=['Pending', 'In Progress']
        ).order_by('deadline')  # type: ignore
    
    @classmethod
    def get_tasks_by_status(cls, status: str) -> models.QuerySet:
        """Get tasks filtered by status."""
        return cls.objects.filter(status=status)  # type: ignore
    
    @classmethod
    def get_tasks_by_priority(cls, priority: int) -> models.QuerySet:
        """Get tasks filtered by priority level."""
        return cls.objects.filter(priority=priority)  # type: ignore


class ContextEntry(models.Model):
    """Context entries (messages, emails, notes) for AI analysis."""
    
    SOURCE_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
        ('Note', 'Note'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(
        help_text="The actual message, email, or note content"
    )
    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        help_text="Type of source"
    )
    processed_insights = models.TextField(
        blank=True,
        null=True,
        help_text="AI-processed insights"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Context Entry"
        verbose_name_plural = "Context Entries"
        ordering = ['-created_at']
        db_table = 'todo_context_entries'
        indexes = [
            models.Index(fields=['source_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.source_type}: {str(self.content)[:30]}"
    
    def clean(self):
        super().clean()
        
        if self.content:
            content = str(self.content).strip()
            if not content:
                raise ValidationError("Content cannot be empty")
    
    @property
    def has_insights(self) -> bool:
        """Check if context entry has processed insights."""
        return bool(self.processed_insights)
    
    @property
    def content_preview(self) -> str:
        """Get first 100 characters of content with ellipsis if longer."""
        content = str(self.content)
        return content[:100] + "..." if len(content) > 100 else content
    
    def update_insights(self, insights: str) -> None:
        """Update processed insights."""
        self.processed_insights = insights
        self.save(update_fields=['processed_insights'])
    
    @classmethod
    def get_by_source_type(cls, source_type: str) -> models.QuerySet:
        """Get context entries filtered by source type."""
        return cls.objects.filter(source_type=source_type)  # type: ignore
    
    @classmethod
    def get_recent_entries(cls, days: int = 7) -> models.QuerySet:
        """Get context entries from last N days."""
        cutoff_date = timezone.now() - timedelta(days=days)
        return cls.objects.filter(created_at__gte=cutoff_date)  # type: ignore
    
    @classmethod
    def get_entries_with_insights(cls) -> models.QuerySet:
        """Get context entries that have processed insights."""
        return cls.objects.filter(processed_insights__isnull=False)  # type: ignore 