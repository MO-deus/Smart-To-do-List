from django.urls import path
from .views import (
    TaskListView, TaskDetailView, CategoryListView, 
    ContextEntryListView, StatisticsView
)
from tasks.ai_views import (
    ai_process_task, ai_create_enhanced_task, ai_health_check, ai_analyze_context,
    ai_suggest_category, ai_enhance_description
)

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<uuid:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('context/', ContextEntryListView.as_view(), name='context-list'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    
    # AI Pipeline endpoints
    path('ai/process-task/', ai_process_task, name='ai-process-task'),
    path('ai/create-enhanced-task/', ai_create_enhanced_task, name='ai-create-enhanced-task'),
    path('ai/analyze-context/', ai_analyze_context, name='ai-analyze-context'),
    path('ai/suggest-category/', ai_suggest_category, name='ai-suggest-category'),
    path('ai/enhance-description/', ai_enhance_description, name='ai-enhance-description'),
    path('ai/health-check/', ai_health_check, name='ai-health-check'),
]