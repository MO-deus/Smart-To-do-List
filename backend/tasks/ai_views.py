import logging
import os
from typing import Dict, Any
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
import asyncio

from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer
from ai_service import AIPipelineController, GeminiAIService

logger = logging.getLogger(__name__)

# Initialize AI services
try:
    gemini_client = GeminiAIService()
    ai_pipeline = AIPipelineController(gemini_client)
    AI_SERVICES_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to initialize AI services: {str(e)}")
    AI_SERVICES_AVAILABLE = False
    ai_pipeline = None

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_process_task(request):
    """
    Process a task through the AI pipeline  
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        task_data = data.get('task', {})
        context_data = data.get('context', None)
        
        if not task_data:
            return Response({
                'error': 'Task data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process task through AI pipeline
        ai_result = asyncio.run(ai_pipeline.process_new_task(task_data, context_data))
        
        if 'error' in ai_result:
            return Response({
                'error': ai_result['error'],
                'status': 'failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'status': 'success',
            'ai_analysis': ai_result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI task processing failed: {str(e)}")
        return Response({
            'error': f'AI processing failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_create_enhanced_task(request):
    """
    Create a task with AI enhancement
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        task_data = data.get('task', {})
        context_data = data.get('context', None)
        auto_create = data.get('auto_create', False)
        
        if not task_data:
            return Response({
                'error': 'Task data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process task through AI pipeline
        ai_result = asyncio.run(ai_pipeline.process_new_task(task_data, context_data))
        
        if 'error' in ai_result:
            return Response({
                'error': ai_result['error'],
                'status': 'failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Extract AI recommendations
        recommendations = ai_result.get('recommendations', {})
        
        # Prepare enhanced task data
        enhanced_task_data = {
            'title': task_data.get('title', ''),
            'description': recommendations.get('enhanced_description', task_data.get('description', '')),
            'priority': recommendations.get('priority_level', 'medium'),
            'deadline': recommendations.get('suggested_deadline', {}).get('deadline') if recommendations.get('suggested_deadline') else None,
        }
        
        # Handle category suggestion
        suggested_category = recommendations.get('suggested_category')
        if suggested_category and suggested_category.get('name'):
            category_name = suggested_category['name']
            category, created = Category.objects.get_or_create(name=category_name)
            enhanced_task_data['category'] = category.id
        
        # Create task if auto_create is enabled
        created_task = None
        if auto_create:
            try:
                serializer = TaskSerializer(data=enhanced_task_data)
                if serializer.is_valid():
                    created_task = serializer.save()
                    task_serializer = TaskSerializer(created_task)
                else:
                    logger.warning(f"Task creation failed: {serializer.errors}")
            except Exception as e:
                logger.error(f"Failed to create task: {str(e)}")
        
        return Response({
            'status': 'success',
            'ai_analysis': ai_result,
            'enhanced_task_data': enhanced_task_data,
            'created_task': TaskSerializer(created_task).data if created_task else None
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI enhanced task creation failed: {str(e)}")
        return Response({
            'error': f'AI processing failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_batch_process_tasks(request):
    """
    Process multiple tasks through the AI pipeline
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        tasks_data = data.get('tasks', [])
        context_data = data.get('context', None)
        
        if not tasks_data:
            return Response({
                'error': 'Tasks data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process tasks through AI pipeline
        ai_results = asyncio.run(ai_pipeline.batch_process_tasks(tasks_data, context_data))
        
        return Response({
            'status': 'success',
            'ai_analyses': ai_results,
            'processed_count': len(ai_results)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI batch processing failed: {str(e)}")
        return Response({
            'error': f'AI batch processing failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def ai_health_check(request):
    """
    Check AI services health
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'status': 'unavailable',
            'message': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'services': {
                'gemini_api': False,
                'ai_pipeline': False
            }
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        health_result = asyncio.run(ai_pipeline.health_check())
        
        return Response({
            'status': 'healthy' if health_result.get('overall_health', False) else 'unhealthy',
            'services': health_result,
            'timestamp': health_result.get('timestamp')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI health check failed: {str(e)}")
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'services': {
                'gemini_api': False,
                'ai_pipeline': False
            }
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET'])
@permission_classes([AllowAny])
def ai_statistics(request):
    """
    Get AI pipeline statistics
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        stats = asyncio.run(ai_pipeline.get_pipeline_statistics())
        
        return Response({
            'status': 'success',
            'statistics': stats
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI statistics retrieval failed: {str(e)}")
        return Response({
            'error': f'Statistics retrieval failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_suggest_category(request):
    """
    Get AI category suggestions for a task
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        task_data = data.get('task', {})
        
        if not task_data:
            return Response({
                'error': 'Task data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get existing categories
        existing_categories = list(Category.objects.values_list('name', flat=True))
        
        # Get AI category suggestions
        category_result = asyncio.run(ai_pipeline.category_suggester.suggest_category(task_data, existing_categories))
        
        return Response({
            'status': 'success',
            'category_suggestions': category_result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI category suggestion failed: {str(e)}")
        return Response({
            'error': f'Category suggestion failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_enhance_task_description(request):
    """
    Enhance task description using AI
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        task_data = data.get('task', {})
        context_data = data.get('context', None)
        
        if not task_data:
            return Response({
                'error': 'Task data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Enhance task description
        enhancement_result = asyncio.run(ai_pipeline.task_enhancer.enhance_task(task_data, context_data))
        
        return Response({
            'status': 'success',
            'enhancement': enhancement_result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI task enhancement failed: {str(e)}")
        return Response({
            'error': f'Task enhancement failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ai_analyze_context(request):
    """
    Analyze context data using AI
    """
    if not AI_SERVICES_AVAILABLE or ai_pipeline is None:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = request.data
        context_data = data.get('context', {})
        
        if not context_data:
            return Response({
                'error': 'Context data is required',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Analyze context
        context_result = asyncio.run(ai_pipeline.context_analyzer.analyze_context(context_data))
        
        return Response({
            'status': 'success',
            'context_analysis': context_result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"AI context analysis failed: {str(e)}")
        return Response({
            'error': f'Context analysis failed: {str(e)}',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 