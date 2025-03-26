from django.db import models

class User(models.Model):
    """
    Represents a user in the system.
    Users can be assigned to multiple tasks via a ManyToMany relationship.
    """

    name = models.CharField(max_length=255)  # User's full name
    email = models.EmailField(unique=True)  # Unique email for authentication/identification
    mobile = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True
    )  # Optional mobile number (nullable & unique)

    def __str__(self):
        """String representation of the User model."""
        return self.name


class Task(models.Model):
    """
    Represents a task that can be assigned to multiple users.
    Tracks task progress and categorization.
    """

    # Task status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Task type choices
    TASK_TYPE_CHOICES = [
        ('feature', 'Feature'),
        ('bugfix', 'Bug Fix'),
        ('enhancement', 'Enhancement'),
        ('documentation', 'Documentation'),
        ('research', 'Research'),
        ('testing', 'Testing'),
        ('deployment', 'Deployment'),
        ('maintenance', 'Maintenance'),
        ('optimization', 'Optimization'),
        ('security', 'Security Update'),
        ('refactor', 'Code Refactor'),
        ('support', 'Customer Support'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]


    name = models.CharField(max_length=255)  # Task title/name
    description = models.TextField(blank=True, null=True)  # Optional task details
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set timestamp on task creation
    completed_at = models.DateTimeField(blank=True, null=True)  # Completion timestamp (nullable)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )  # task progress status
    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        default='feature'
    ) # priority
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    # Categorization of the task
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_tasks'
    )  # Many-to-Many relationship: A task can have multiple assigned users

    def __str__(self):
        """String representation of the Task model."""
        return self.name
