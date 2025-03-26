from django.contrib import admin
from .models import User, Task


class TaskInline(admin.TabularInline):
    """ Inline task display in the User admin panel. """
    model = Task.assigned_users.through
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'task_type', 'priority', 'status', 'created_at', 'assigned_user_info')  # Added assigned_user_info
    list_filter = ('status', 'priority', 'task_type')
    search_fields = ('name', 'description')
    ordering = ('priority', 'created_at')

    def assigned_user_info(self, obj):
        """ Returns assigned user ID and name. """
        assigned_users = obj.assigned_users.all()  # Fetch all assigned users
        if assigned_users:
            return ", ".join([f"{user.id} - {user.name}" for user in assigned_users])
        return "Unassigned"

    assigned_user_info.short_description = "Assigned Users"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Custom admin configuration for users """
    list_display = ("id", "name", "email", "mobile", "get_tasks_by_type")
    search_fields = ("name", "email", "mobile")
    ordering = ("name",)
    inlines = [TaskInline]

    def get_tasks_by_type(self, obj):
        """ Returns a formatted string of tasks assigned to the user, grouped by task type. """
        tasks = Task.objects.filter(assigned_users=obj)  #  Correctly fetch tasks
        task_summary = {}

        for task in tasks:
            if task.task_type in task_summary:
                task_summary[task.task_type].append(task.name)
            else:
                task_summary[task.task_type] = [task.name]

        return ", ".join([f"{task_type}: {', '.join(names)}" for task_type, names in task_summary.items()])

    get_tasks_by_type.short_description = "Assigned Tasks (by Type)"  # Column header name
