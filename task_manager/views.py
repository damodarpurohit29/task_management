from django.contrib.sites import requests
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer, TaskAssignSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def choose_redirect(request):
    return render(request, "redirect_choice.html")


def login_view(request):
    """
    Handles user login (Google OAuth and manual login).
    """
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('choose_redirect')  # ✅ Fix redirect issue
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    # Google OAuth URL
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=email profile"
    )

    return render(request, "login.html", {"google_auth_url": google_auth_url})


def google_callback_view(request):
    """
    Handles Google OAuth callback.
    """
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    # Exchange code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        return JsonResponse({"error": "Failed to get access token"}, status=400)

    access_token = token_json["access_token"]

    # Get user info from Google
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    # Check if user exists, if not create one
    user, created = User.objects.get_or_create(username=user_info["email"])  # ✅ Fix user creation
    if created:
        user.email = user_info["email"]
        user.set_unusable_password()  # Prevents password login
        user.save()

    # Log the user in
    login(request, user)
    return redirect('choose_redirect')  #   redirect main url


def logout_view(request):
    """Handle logout and redirect to home."""
    logout(request)
    return HttpResponseRedirect('/')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage Users.
    Supports CRUD operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskCreateView(generics.CreateAPIView):
    """
    API to create a new task.
    Accepts task details and returns the created task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAssignView(APIView):
    """
    API to assign users to a task.
    Accepts a list of user IDs in request body.
    """

    @swagger_auto_schema(
        request_body=TaskAssignSerializer,
        responses={
            200: "Users assigned successfully!",
            400: "Invalid data or task not found"
        }
    )
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskAssignSerializer(data=request.data)

        if serializer.is_valid():
            user_ids = serializer.validated_data["user_ids"]
            users = User.objects.filter(id__in=user_ids)

            if not users.exists():
                return Response({"error": "No valid users found"}, status=status.HTTP_400_BAD_REQUEST)

            task.assigned_users.set(users)  # Assign users
            return Response({"message": "Users assigned successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTasksView(APIView):
    """
    API to fetch all tasks assigned to a specific user.
    """

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        tasks = Task.objects.filter(assigned_users=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskListView(generics.ListAPIView):
    """
    API to list all tasks.
    Supports optional filtering by status and task_type.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        task_type_filter = self.request.query_params.get('task_type')

        filters = {}
        if status_filter:
            filters["status"] = status_filter
        if task_type_filter:
            filters["task_type"] = task_type_filter

        return queryset.filter(**filters)


class TaskUpdateView(generics.UpdateAPIView):
    """
    API to update a task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDeleteView(generics.DestroyAPIView):
    """
    API to delete a task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer