from django.urls import path
from .views import (
    CategoryCreate, TaskList, TaskDetail, CategoryList, ContextEntryList,
    ContextEntryCreate, AISuggestions
)
from tasks.ai_views import (
    ai_process_task, ai_create_enhanced_task, ai_batch_process_tasks,
    ai_health_check, ai_statistics, ai_suggest_category,
    ai_enhance_task_description, ai_analyze_context
)

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('context/', ContextEntryList.as_view(), name='context-list'),
    path('context/create/', ContextEntryCreate.as_view(), name='context-create'),
    path('ai/suggestions/', AISuggestions.as_view(), name='ai-suggestions'),
    path('categories/create/', CategoryCreate.as_view(), name='category-create'),
    
    # AI Pipeline endpoints
    path('ai/process-task/', ai_process_task, name='ai-process-task'),
    path('ai/create-enhanced-task/', ai_create_enhanced_task, name='ai-create-enhanced-task'),
    path('ai/batch-process/', ai_batch_process_tasks, name='ai-batch-process'),
    path('ai/health-check/', ai_health_check, name='ai-health-check'),
    path('ai/statistics/', ai_statistics, name='ai-statistics'),
    path('ai/suggest-category/', ai_suggest_category, name='ai-suggest-category'),
    path('ai/enhance-description/', ai_enhance_task_description, name='ai-enhance-description'),
    path('ai/analyze-context/', ai_analyze_context, name='ai-analyze-context'),
]