# from django.db import models
# from user.models import User

# # Create your models here.

# class Ticket(models.Model):
    
#     TYPE_CHOICES = [
#     ('bug', 'Bug'),
#     ('task', 'Task')
#     ]

#     PRIORITY_CHOICES = [
#     ('critical', 'Critical'),
#     ('high', 'High'),
#     ('medium', 'Medium'),
#     ('low', 'Low')
#     ]
    
#     STATUS_CHOICES = [
#     ('open', 'Open'),
#     ('in_progress', 'In Progress'),
#     ('closed', 'Closed'),
#     ('resolved', 'Resolved')
#     ]
    
#     number = models.AutoField(primary_key=True)  # Automatically generated
#     task_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     assignee = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.SET_NULL, null=True, blank=True)
#     creator = models.ForeignKey(User, related_name='tasks_created', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     attachment = models.URLField(max_length=255, blank=True)
#     blocking_tasks = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocked_by')



from django.db import models
from uuid import uuid4
from django.utils import timezone
from user.models import User  # Assuming User model is in the user app


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To do'),
        ('in_progress', 'In progress'),
        ('code_review', 'Code review'),
        ('dev_test', 'Dev test'),
        ('testing', 'Testing'),
        ('done', 'Done'),
        ('wontfix', 'Wontfix'),
    ]

    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    TYPE_CHOICES = [
        ('bug', 'Bug'),
        ('task', 'Task'),
    ]

    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number = models.AutoField(unique=True, primary_key=True)  # Automatically generated
    task_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='task')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    attachment = models.URLField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    blocking_tasks = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by_tasks', blank=True)

    def __str__(self):
        return f"Task {self.number}: {self.title}"
