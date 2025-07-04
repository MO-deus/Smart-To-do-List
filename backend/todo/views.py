from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, Category, ContextEntry
from .serializers import TaskSerializer, CategorySerializer, ContextEntrySerializer
# Create your views here.

# This view returns all tasks in the database and can create new tasks
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# This view handles individual task operations (GET, PUT, DELETE)
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
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

# Add new context entry
class ContextEntryCreate(generics.CreateAPIView):
    queryset = ContextEntry.objects.all()
    serializer_class = ContextEntrySerializer

# AI-powered suggestions (stub)
class AISuggestions(APIView):
    def post(self, request):
        # For now, just echo back the input and a dummy suggestion
        return Response({
            "suggestion": "This is a dummy AI suggestion.",
            "input": request.data
        })

#Creating categories
class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer