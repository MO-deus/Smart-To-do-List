from django.urls import path
from .views import (
    CategoryCreate, TaskList, TaskDetail, CategoryList, ContextEntryList,
    ContextEntryCreate, AISuggestions
)

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('context/', ContextEntryList.as_view(), name='context-list'),
    path('context/create/', ContextEntryCreate.as_view(), name='context-create'),
    path('ai/suggestions/', AISuggestions.as_view(), name='ai-suggestions'),
    path('categories/create/', CategoryCreate.as_view(), name='category-create'),
]