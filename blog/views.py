# Import necessary Django and DRF modules
from django.shortcuts import render
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Category, BlogPost, Tag
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .permissions import IsAuthorOrReadOnly
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema


# View for creating a new blog post
class CreatePostView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    # Custom logic to save category and tags with the post
    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        
        # Check if the provided category exists
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise ValidationError({'message': 'Category does not exist.'})

        # Save the post with the current user as author
        blog_post = serializer.save(author=self.request.user)

        # Add tags to the post if provided
        tags_data = self.request.data.get('tags', [])
        if tags_data:
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog_post.tags.add(tag)

        blog_post.save()

    @swagger_auto_schema(operation_summary="Create a new post.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# View for retrieving the details of a single post
class PostDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


# Pagination class for blog posts list view
class BlogPostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100  # Set a limit on the maximum page size


# View for listing all blog posts with filtering, sorting, and pagination
class PostListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category_id', 'author_id']

    # Define ordering based on query parameter 'order'
    def get_queryset(self):
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            return BlogPost.objects.all().order_by('-created_date')
        return BlogPost.objects.all().order_by('created_date')
    
    @swagger_auto_schema(operation_summary="List all posts.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# View for updating a blog post
class PostUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    @swagger_auto_schema(operation_summary="Update a post")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


# View for deleting a blog post
class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = BlogPost.objects.all()

    @swagger_auto_schema(operation_summary="Delete a post")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ViewSet for managing categories
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ViewSet for managing tags
class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# View for listing all posts within a specific category
class PostByCategoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        # Filter posts by category ID from URL
        category_id = self.kwargs.get('pk')
        return BlogPost.objects.filter(category__id=category_id)


# View for listing all posts by a specific author
class PostByAuthorView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        # Filter posts by author ID from URL
        author_id = self.kwargs.get('pk')
        return BlogPost.objects.filter(author__id=author_id)


# View for searching blog posts by title, content, tags, or author name
class BlogPostSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    @swagger_auto_schema(operation_summary="Search for a post.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Filter posts by search query across various fields
        queryset = BlogPost.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(author__username__icontains=search_query)
            ).distinct()

        return queryset

