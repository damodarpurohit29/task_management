from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskCreateView, TaskAssignView, UserTasksView, TaskListView,
    TaskUpdateView, TaskDeleteView, UserViewSet, TaskDetailView,
    login_view, choose_redirect
)

# Initialize DRF's DefaultRouter to handle user-related API endpoints automatically
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # Registers a user API endpoint under `/users/`

urlpatterns = [
    #  Authentication Endpoints
    path('', login_view, name='login'),  # Login Page
    path('redirect/', choose_redirect, name='choose_redirect'),  # Redirect choice page

    #  Task Management Endpoints
    path('tasks/', TaskListView.as_view(), name='task-list'),  # List all tasks (GET)
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),  # Create a new task (POST)
    path('tasks/<int:task_id>/assign/', TaskAssignView.as_view(), name='task-assign'),  # Assign users to a task (POST)
    path('tasks/user/<int:user_id>/', UserTasksView.as_view(), name='user-tasks'),  # Retrieve user tasks (GET)
    path('tasks/<int:pk>/detail/', TaskDetailView.as_view(), name='task-detail'),  # Retrieve task details (GET)
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),  # Update a task (PUT/PATCH)
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),  # Delete a task (DELETE)

    #  User Management Endpoints (Handled by DRF's DefaultRouter)
    path('', include(router.urls)),  # Includes all user-related API routes
]