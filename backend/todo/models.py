from django.db import models

# This model is for categories or tags for tasks
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # name of the category
    usage_frequency = models.IntegerField(default=0)      # how many times this category is used

    def __str__(self):
        return self.name

# This model is for tasks in the todo list
class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)  # title of the task
    description = models.TextField(blank=True) # description of the task
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # category of the task
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2) # priority of the task
    deadline = models.DateTimeField(null=True, blank=True) # deadline for the task
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') # status of the task
    created_at = models.DateTimeField(auto_now_add=True) # when the task was created
    updated_at = models.DateTimeField(auto_now=True)     # when the task was last updated
    priority_score = models.FloatField(null=True, blank=True) # AI-computed priority score

    def __str__(self):
        return self.title

# This model is for storing context entries like messages, emails, notes
class ContextEntry(models.Model):
    SOURCE_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
        ('Note', 'Note'),
    ]
    content = models.TextField() # the actual message, email, or note
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES) # where the context came from
    processed_insights = models.TextField(blank=True, null=True) # AI-processed insights (optional)
    created_at = models.DateTimeField(auto_now_add=True) # when the context was added

    def __str__(self):
        # Show the source type and the first 30 characters of the content
        return f"{self.source_type}: {self.content[:30]}"
