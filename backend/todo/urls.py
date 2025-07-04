from django.urls import path
from .views import TaskList, CategoryList, ContextEntryList

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),  # GET all tasks
    path('categories/', CategoryList.as_view(), name='category-list'),  # GET all categories
    path('context/', ContextEntryList.as_view(), name='context-list'),  # GET all context entries
] 