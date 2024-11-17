# URL configuration for the config project.

from django.contrib import admin
from django.urls import path, include

# Importing for API documentation generation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Set up the schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",  # Title for the API
        default_version='v1',  # Version of the API
        description="Blog API documentation",  # Description of what the API does
        contact=openapi.Contact(email="mannnie55@gmail.com"),  # Contact email for the API
        license=openapi.License(name="BSD License"),  # API license info
    ),
    public=True,  # Makes the schema public
    permission_classes=(permissions.AllowAny,)  # Allows any user to access the documentation
)

urlpatterns = [
    # API Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI for API docs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI for API docs

    # API Endpoints
    path("api/users/", include("users.urls")),  # Include URLs from the 'users' app
    path("api/blog/", include("blog.urls")),  # Include URLs from the 'blog' app
    path("api/comment/", include("comment.urls")),  # Include URLs from the 'comment' app

    # Admin Interface
    path("admin/", admin.site.urls),  # Django admin interface
]
