"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.views import LogoutView
from task_manager.views import login_view, choose_redirect, logout_view
from django.contrib.auth import views as auth_views

# Swagger API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version="v1",
        description="API documentation for the Task Management system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Task Management App URLs
    path('api/', include('task_manager.urls')),

    # Authentication
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/logout/', RedirectView.as_view(url='/logout/'), name='accounts-logout'),
    # path("logout/", LogoutView.as_view(next_page='/login'), name="logout"),
    path("choose-redirect/", choose_redirect, name="choose-redirect"),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Google OAuth
    path('auth/', include('social_django.urls', namespace='social')),

    # API Documentation (Swagger & ReDoc)
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]