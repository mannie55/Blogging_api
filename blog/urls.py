# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TagViewSet,
    PostListView,
    CreatePostView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostByCategoryView,
    PostByAuthorView,
    BlogPostSearchView,
)

# Set up a router for category and tag viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

# Define app namespace
app_name = 'blog'

urlpatterns = [
    # Router URLs for category and tag viewsets
    path('', include(router.urls)),

    # Post-specific paths
    path('posts/', PostListView.as_view(), name='post-list'),              # List all posts
    path('posts/create/', CreatePostView.as_view(), name='post-create'),    # Create a new post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Retrieve a single post
    path('posts/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),  # Update a specific post
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),  # Delete a specific post

    # Custom filtering paths
    path('posts/category/<int:pk>/', PostByCategoryView.as_view(), name='posts-by-category'),  # Filter posts by category
    path('posts/author/<int:pk>/', PostByAuthorView.as_view(), name='posts-by-author'),       # Filter posts by author
    path('posts/search/', BlogPostSearchView.as_view(), name='post-search'),                  # Search for posts
]
