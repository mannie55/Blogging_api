# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PostListView, CreatePostView, PostDetailView, PostUpdateView, PostDeleteView, TagViewSet, PostByCategoryView, PostByAuthorView, BlogPostSearchView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/category/<int:id>/', PostByCategoryView.as_view(), name='posts-by-category'),
    path('posts/search/', BlogPostSearchView.as_view(), name='post-search'),
    path('posts/author/<int:id>/', PostByAuthorView.as_view(), name='posts-by-author'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', CreatePostView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  
    path('posts/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]
