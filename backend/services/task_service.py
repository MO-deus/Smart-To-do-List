"""Task service for handling task-related business logic."""

import logging
from typing import Dict, List, Any, Optional, cast
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.exceptions import ValidationError

from .base_service import BaseService
from todo.models import Task, Category
from todo.serializers import TaskSerializer


class TaskService(BaseService[Task]):
    """Service for task operations."""
    
    def __init__(self):
        super().__init__(Task, TaskSerializer)
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        valid_statuses = ['Pending', 'In Progress', 'Completed']
        if status not in valid_statuses:
            raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
        return self.get_all(status=status)
    
    def get_tasks_by_priority(self, priority: int) -> List[Dict[str, Any]]:
        valid_priorities = [1, 2, 3]
        if priority not in valid_priorities:
            raise ValidationError(f"Invalid priority. Must be one of: {valid_priorities}")
        return self.get_all(priority=priority)
    
    def get_tasks_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        return self.get_all(category_id=category_id)
    
    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        try:
            now = datetime.now()
            overdue_tasks = self.model.objects.filter(  # type: ignore
                deadline__lt=now,
                status__in=['Pending', 'In Progress']
            )  # type: ignore
            serializer = self.serializer_class(overdue_tasks, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve overdue tasks: {str(e)}")
            raise
    
    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict[str, Any]]:
        try:
            now = datetime.now()
            future_date = now + timedelta(days=days)
            
            upcoming_tasks = self.model.objects.filter(  # type: ignore
                deadline__gte=now,
                deadline__lte=future_date,
                status__in=['Pending', 'In Progress']
            ).order_by('deadline')  # type: ignore
            
            serializer = self.serializer_class(upcoming_tasks, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve upcoming deadlines: {str(e)}")
            raise
    
    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        try:
            search_tasks = self.model.objects.filter(  # type: ignore
                Q(title__icontains=query) | Q(description__icontains=query)
            )  # type: ignore
            serializer = self.serializer_class(search_tasks, many=True)
            return cast(List[Dict[str, Any]], serializer.data)
        except Exception as e:
            self.logger.error(f"Failed to search tasks: {str(e)}")
            raise
    
    def update_task_status(self, task_id: str, status: str) -> Optional[Dict[str, Any]]:
        valid_statuses = ['Pending', 'In Progress', 'Completed']
        if status not in valid_statuses:
            raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
        return self.update(task_id, {'status': status})
    
    def update_task_priority(self, task_id: str, priority: int) -> Optional[Dict[str, Any]]:
        valid_priorities = [1, 2, 3]
        if priority not in valid_priorities:
            raise ValidationError(f"Invalid priority. Must be one of: {valid_priorities}")
        return self.update(task_id, {'priority': priority})
    
    def assign_category(self, task_id: str, category_id: str) -> Optional[Dict[str, Any]]:
        return self.update(task_id, {'category': category_id})
    
    def get_task_statistics(self) -> Dict[str, Any]:
        try:
            total_tasks = self.model.objects.count()  # type: ignore
            pending_tasks = self.model.objects.filter(status='Pending').count()  # type: ignore
            in_progress_tasks = self.model.objects.filter(status='In Progress').count()  # type: ignore
            completed_tasks = self.model.objects.filter(status='Completed').count()  # type: ignore
            overdue_tasks = self.model.objects.filter(  # type: ignore
                deadline__lt=datetime.now(),
                status__in=['Pending', 'In Progress']
            ).count()  # type: ignore
            
            return {
                'total_tasks': total_tasks,
                'pending_tasks': pending_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completed_tasks': completed_tasks,
                'overdue_tasks': overdue_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        except Exception as e:
            self.logger.error(f"Failed to get task statistics: {str(e)}")
            raise 