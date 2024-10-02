from django.shortcuts import render
from .serializers import BlogPostSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Category, BlogPost
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from .permissions import IsAuthorOrReadOnly
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters




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

        serializer.save(author=self.request.user)


class PostDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'uid'


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
    search_fields = ['author__username', 'content', 'category__name']
    

    def get_queryset(self):
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            return BlogPost.objects.all().order_by('-created_date')
        return BlogPost.objects.all().order_by('created_date')

class PostUpdateView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uid"


class PostDeleteView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uid"

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer