"""Enhanced views using service layer for business logic and OOP practices."""

import logging
from typing import Dict, Any
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from services import TaskService, CategoryService, ContextService, AIServiceFactory

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    """Base API view with common error handling, logging, and response formatting."""
    
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_service = TaskService()
        self.category_service = CategoryService()
        self.context_service = ContextService()
        self.ai_factory = AIServiceFactory()
    
    def handle_exception(self, exc):
        """Handle exceptions and return appropriate error responses."""
        if isinstance(exc, ValidationError):
            logger.warning(f"Validation error: {str(exc)}")
            return Response({
                'error': 'Validation error',
                'details': str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.error(f"Unexpected error: {str(exc)}")
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskListView(BaseAPIView):
    """View for task list operations using TaskService for business logic."""
    
    def get(self, request):
        """Get all tasks with optional filtering by status, priority, category, or search."""
        try:
            status_filter = request.query_params.get('status')
            priority_filter = request.query_params.get('priority')
            category_filter = request.query_params.get('category')
            search_query = request.query_params.get('search')
            
            if search_query:
                tasks = self.task_service.search_tasks(search_query)
            elif status_filter:
                tasks = self.task_service.get_tasks_by_status(status_filter)
            elif priority_filter:
                try:
                    priority = int(priority_filter)
                    tasks = self.task_service.get_tasks_by_priority(priority)
                except ValueError:
                    return Response({
                        'error': 'Invalid priority value'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif category_filter:
                tasks = self.task_service.get_tasks_by_category(category_filter)
            else:
                tasks = self.task_service.get_all()
            
            return Response({
                'status': 'success',
                'data': tasks,
                'count': len(tasks)
            })
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error retrieving tasks: {str(e)}")
            return Response({
                'error': 'Failed to retrieve tasks'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create a new task with title, description, category, priority, and deadline."""
        try:
            task_data = request.data
            created_task = self.task_service.create(task_data)
            
            return Response({
                'status': 'success',
                'message': 'Task created successfully',
                'data': created_task
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return Response({
                'error': 'Failed to create task'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDetailView(BaseAPIView):
    """View for individual task operations (get, update, delete) using TaskService."""
    
    def get(self, request, task_id):
        """Get a specific task by UUID."""
        try:
            task = self.task_service.get_by_id(task_id)
            
            if task is None:
                return Response({
                    'error': 'Task not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'status': 'success',
                'data': task
            })
            
        except Exception as e:
            logger.error(f"Error retrieving task {task_id}: {str(e)}")
            return Response({
                'error': 'Failed to retrieve task'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, task_id):
        """Update a specific task by UUID with any task fields."""
        try:
            task_data = request.data
            updated_task = self.task_service.update(task_id, task_data)
            
            if updated_task is None:
                return Response({
                    'error': 'Task not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'status': 'success',
                'message': 'Task updated successfully',
                'data': updated_task
            })
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            return Response({
                'error': 'Failed to update task'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, task_id):
        """Delete a specific task by UUID."""
        try:
            deleted = self.task_service.delete(task_id)
            
            if not deleted:
                return Response({
                    'error': 'Task not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'status': 'success',
                'message': 'Task deleted successfully'
            })
            
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            return Response({
                'error': 'Failed to delete task'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListView(BaseAPIView):
    """View for category list operations using CategoryService for business logic."""
    
    def get(self, request):
        """Get all categories with optional filtering by min_usage or search."""
        try:
            min_usage = request.query_params.get('min_usage')
            search_query = request.query_params.get('search')
            
            if search_query:
                categories = self.category_service.search_categories(search_query)
            elif min_usage:
                try:
                    min_usage_int = int(min_usage)
                    categories = self.category_service.get_categories_by_usage(min_usage_int)
                except ValueError:
                    return Response({
                        'error': 'Invalid min_usage value'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                categories = self.category_service.get_all()
            
            return Response({
                'status': 'success',
                'data': categories,
                'count': len(categories)
            })
            
        except Exception as e:
            logger.error(f"Error retrieving categories: {str(e)}")
            return Response({
                'error': 'Failed to retrieve categories'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create a new category with name."""
        try:
            category_data = request.data
            created_category = self.category_service.create(category_data)
            
            return Response({
                'status': 'success',
                'message': 'Category created successfully',
                'data': created_category
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return Response({
                'error': 'Failed to create category'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContextEntryListView(BaseAPIView):
    """View for context entry list operations using ContextService for business logic."""
    
    def get(self, request):
        """Get all context entries with optional filtering by source_type, days, or search."""
        try:
            source_type = request.query_params.get('source_type')
            days = request.query_params.get('days')
            search_query = request.query_params.get('search')
            
            if search_query:
                entries = self.context_service.search_context(search_query)
            elif source_type:
                entries = self.context_service.get_context_by_source_type(source_type)
            elif days:
                try:
                    days_int = int(days)
                    entries = self.context_service.get_recent_context(days_int)
                except ValueError:
                    return Response({
                        'error': 'Invalid days value'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                entries = self.context_service.get_all()
            
            return Response({
                'status': 'success',
                'data': entries,
                'count': len(entries)
            })
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error retrieving context entries: {str(e)}")
            return Response({
                'error': 'Failed to retrieve context entries'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create a new context entry with content, source_type, and optional processed_insights."""
        try:
            entry_data = request.data
            created_entry = self.context_service.create(entry_data)
            
            return Response({
                'status': 'success',
                'message': 'Context entry created successfully',
                'data': created_entry
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'error': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating context entry: {str(e)}")
            return Response({
                'error': 'Failed to create context entry'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatisticsView(BaseAPIView):
    """View for providing application statistics about tasks, categories, and context."""
    
    def get(self, request):
        """Get comprehensive application statistics by type (tasks, categories, context, all)."""
        try:
            stats_type = request.query_params.get('type', 'all')
            
            if stats_type == 'tasks':
                statistics = self.task_service.get_task_statistics()
            elif stats_type == 'categories':
                statistics = self.category_service.get_category_statistics()
            elif stats_type == 'context':
                statistics = self.context_service.get_context_statistics()
            elif stats_type == 'all':
                statistics = {
                    'tasks': self.task_service.get_task_statistics(),
                    'categories': self.category_service.get_category_statistics(),
                    'context': self.context_service.get_context_statistics(),
                    'ai_services': self.ai_factory.health_check()
                }
            else:
                return Response({
                    'error': 'Invalid statistics type'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'status': 'success',
                'data': statistics
            })
            
        except Exception as e:
            logger.error(f"Error retrieving statistics: {str(e)}")
            return Response({
                'error': 'Failed to retrieve statistics'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 