"""Optimized AI views for the todo application using consolidated service layer."""

import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError

from services import TaskService, CategoryService, ContextService, AIServiceFactory

logger = logging.getLogger(__name__)


class BaseAIView(APIView):
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_service = TaskService()
        self.category_service = CategoryService()
        self.context_service = ContextService()
        self.ai_factory = AIServiceFactory()
    
    def check_ai_availability(self) -> bool:
        return self.ai_factory.services_available
    
    def get_ai_pipeline(self):
        return self.ai_factory.get_ai_pipeline()
    
    def get_consolidated_ai(self):
        return self.ai_factory.get_consolidated_ai()
    
    def handle_ai_unavailable(self) -> Response:
        return Response({
            'error': 'AI services are not available. Please check GEMINI_API_KEY configuration.',
            'status': 'unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def handle_exception(self, exc):
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


class AIProcessTaskView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
        try:
            data = request.data
            task_data = data.get('task', {})
            context_data = data.get('context', None)
            
            if not task_data:
                return Response({
                    'error': 'Task data is required',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Process task through optimized AI pipeline
            ai_pipeline = self.get_ai_pipeline()
            if not ai_pipeline:
                return self.handle_ai_unavailable()
            
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


class AICreateEnhancedTaskView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
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
            
            # Process task through optimized AI pipeline
            ai_pipeline = self.get_ai_pipeline()
            if not ai_pipeline:
                return self.handle_ai_unavailable()
            
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
                'title': recommendations.get('enhanced_title', task_data.get('title', '')),
                'description': recommendations.get('enhanced_description', task_data.get('description', '')),
                'priority': recommendations.get('priority_level', 'medium'),
                'deadline': recommendations.get('suggested_deadline'),  # Already a string from pipeline
            }
            
            # Handle category suggestion
            suggested_category = recommendations.get('suggested_category')
            if suggested_category and suggested_category.get('name'):
                category_name = suggested_category['name']
                category_data = self.category_service.create_category_if_not_exists(category_name)
                enhanced_task_data['category'] = category_data['id']
            
            # Create task if auto_create is enabled
            created_task = None
            if auto_create:
                try:
                    created_task = self.task_service.create(enhanced_task_data)
                except Exception as e:
                    logger.error(f"Failed to create enhanced task: {str(e)}")
            
            return Response({
                'status': 'success',
                'ai_analysis': ai_result,
                'enhanced_task_data': enhanced_task_data,
                'created_task': created_task
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"AI enhanced task creation failed: {str(e)}")
            return Response({
                'error': f'AI processing failed: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIBatchProcessView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
        try:
            data = request.data
            tasks_data = data.get('tasks', [])
            context_data = data.get('context', None)
            
            if not tasks_data:
                return Response({
                    'error': 'Tasks data is required',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Process tasks through optimized AI pipeline
            ai_pipeline = self.get_ai_pipeline()
            if not ai_pipeline:
                return self.handle_ai_unavailable()
            
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


class AIHealthCheckView(BaseAIView):
    def get(self, request):
        try:
            health_status = self.ai_factory.health_check()
            model_info = self.ai_factory.get_model_info()
            
            return Response({
                'status': 'success',
                'ai_health': health_status,
                'model_info': model_info
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"AI health check failed: {str(e)}")
            return Response({
                'error': f'AI health check failed: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AISuggestCategoryView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
        try:
            data = request.data
            task_title = data.get('task_title', '')
            task_description = data.get('task_description', '')
            context_data = data.get('context', None)
            
            if not task_title and not task_description:
                return Response({
                    'error': 'Task title or description is required',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use consolidated AI service for category suggestion
            consolidated_ai = self.get_consolidated_ai()
            if not consolidated_ai:
                return self.handle_ai_unavailable()
            
            # Create task data for analysis
            task_data = {
                'title': task_title,
                'description': task_description
            }
            
            # Generate suggestions using comprehensive analysis
            analysis = asyncio.run(consolidated_ai.comprehensive_task_analysis(task_data, context_data))
            
            suggestions = analysis.get('category_suggestion', {})
            
            return Response({
                'status': 'success',
                'suggestions': suggestions
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"AI category suggestion failed: {str(e)}")
            return Response({
                'error': f'AI category suggestion failed: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIEnhanceTaskDescriptionView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
        try:
            data = request.data
            task_title = data.get('task_title', '')
            task_description = data.get('task_description', '')
            context_data = data.get('context', None)
            
            if not task_title:
                return Response({
                    'error': 'Task title is required',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use consolidated AI service for description enhancement
            consolidated_ai = self.get_consolidated_ai()
            if not consolidated_ai:
                return self.handle_ai_unavailable()
            
            # Create task data for analysis
            task_data = {
                'title': task_title,
                'description': task_description
            }
            
            # Enhance description using comprehensive analysis
            analysis = asyncio.run(consolidated_ai.comprehensive_task_analysis(task_data, context_data))
            
            enhanced_description = analysis.get('task_enhancement', {}).get('enhanced_description', '')
            
            return Response({
                'status': 'success',
                'enhanced_description': enhanced_description
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"AI task description enhancement failed: {str(e)}")
            return Response({
                'error': f'AI task description enhancement failed: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIAnalyzeContextView(BaseAIView):
    def post(self, request):
        if not self.check_ai_availability():
            return self.handle_ai_unavailable()
        
        try:
            data = request.data
            context_data = data.get('context', {})
            
            # Handle both string and object formats for backward compatibility
            if isinstance(context_data, str):
                # If it's a string, convert to the expected format
                context_data = {
                    'content': context_data,
                    'source': 'manual_input',
                    'timestamp': datetime.now().isoformat()
                }
            elif isinstance(context_data, dict):
                # If it's already an object, ensure it has the required fields
                if 'content' not in context_data:
                    return Response({
                        'error': 'Context data must contain "content" field',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Context data must be a string or object',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not context_data.get('content', '').strip():
                return Response({
                    'error': 'Context content is required',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use consolidated AI service for context analysis
            consolidated_ai = self.get_consolidated_ai()
            if not consolidated_ai:
                return self.handle_ai_unavailable()
            
            # Analyze context using consolidated service
            analysis_result = asyncio.run(consolidated_ai.context_analysis(context_data))
            
            return Response({
                'status': 'success',
                'analysis': analysis_result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"AI context analysis failed: {str(e)}")
            return Response({
                'error': f'AI context analysis failed: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function-based views for backward compatibility
@api_view(['POST'])
@permission_classes([AllowAny])
def ai_process_task(request):
    view = AIProcessTaskView()
    return view.post(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_create_enhanced_task(request):
    view = AICreateEnhancedTaskView()
    return view.post(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_analyze_context(request):
    view = AIAnalyzeContextView()
    return view.post(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_suggest_category(request):
    view = AISuggestCategoryView()
    return view.post(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_enhance_description(request):
    view = AIEnhanceTaskDescriptionView()
    return view.post(request)


@api_view(['GET'])
@permission_classes([AllowAny])
def ai_health_check(request):
    view = AIHealthCheckView()
    return view.get(request) 