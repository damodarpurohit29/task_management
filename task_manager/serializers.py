from rest_framework import serializers
from .models import Task, User

class TaskSummarySerializer(serializers.ModelSerializer):
    """
    A simplified Task serializer used inside UserSerializer.
    This ensures assigned tasks are displayed without exposing assigned_users.
    """

    class Meta:
        model = Task
        fields = ["id", "name", "description", "completed_at", "status", "task_type"]

class TaskSerializer(serializers.ModelSerializer):
    """
    Full serializer for the Task model.
    Includes assigned_users details when directly retrieving tasks.
    """

    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )

    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "name", "description", "completed_at", "status", "task_type","priority", "user_ids", "assigned_users"]

    def get_assigned_users(self, obj):
        """Returns a list of assigned user IDs for the task."""
        return [user.id for user in obj.assigned_users.all()]

    def create(self, validated_data):
        """Handles user assignment when creating a task."""
        user_ids = validated_data.pop("user_ids", [])
        task = Task.objects.create(**validated_data)
        task.assigned_users.set(User.objects.filter(id__in=user_ids))
        return task

class TaskAssignSerializer(serializers.Serializer):
    """
    Serializer for assigning users to an existing task.
    Used in the `tasks/{task_id}/assign/` endpoint.
    """

    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of user IDs to assign"
    )

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Displays only assigned tasks using TaskSummarySerializer.
    """

    assigned_tasks = TaskSummarySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "mobile" ,"assigned_tasks"]
