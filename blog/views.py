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



class CreatePostView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Override the perform_create method to handle custom saving."""
        category_id = self.request.data.get('category')
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise ValidationError({'message': 'Category does not exist.'})

        blog_post = serializer.save(author=self.request.user)

        tags_data = self.request.data.get('tags', [])
        if tags_data:
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog_post.tags.add(tag)

        blog_post.save()

    @swagger_auto_schema(operation_summary="create a new post.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class PostDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer




class BlogPostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100  # Limit maximum page size

class PostListView(ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow anyone to read
    pagination_class = BlogPostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category_id', 'author_id']

    def get_queryset(self):
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            return BlogPost.objects.all().order_by('-created_date')
        return BlogPost.objects.all().order_by('created_date')
    
    @swagger_auto_schema(operation_summary="List all posts.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class PostUpdateView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(operation_summary="Update a post")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)



class PostDeleteView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(operation_summary="Delete a post")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostByCategoryView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('pk') # Get category ID from the URL
        return BlogPost.objects.filter(category__id=category_id)
    

class PostByAuthorView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

   
    def get_queryset(self):
        author_id = self.kwargs.get('pk')  # Get author ID from the URL
        return BlogPost.objects.filter(author__id=author_id)
    


class BlogPostSearchView(ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="search for a post.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = BlogPost.objects.all()  # Start with all blog posts
        search_query = self.request.query_params.get('search', None)  # Get the search query

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(author__username__icontains=search_query)
            ).distinct()  # Use distinct to avoid duplicates

        return queryset
