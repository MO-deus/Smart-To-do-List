from django.shortcuts import render
from rest_framework import generics
from .models import Task, Category, ContextEntry
from .serializers import TaskSerializer, CategorySerializer, ContextEntrySerializer

# Create your views here.

# This view returns all tasks in the database
class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# This view returns all categories/tags
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# This view returns all context entries
class ContextEntryList(generics.ListAPIView):
    queryset = ContextEntry.objects.all()
    serializer_class = ContextEntrySerializer
