# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PostListView, CreatePostView, PostDetailView, PostUpdateView, PostDeleteView

router = DefaultRouter()
router.register(r'', CategoryViewSet)

urlpatterns = [
    path('categories/', include(router.urls)),
    path('', PostListView.as_view(), name='post-list'),
    path('posts/create/', CreatePostView.as_view(), name='post-create'),
    path('posts/<uuid:uid>/', PostDetailView.as_view(), name='post-detail'),  
    path('posts/update/<uuid:uid>/', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/<uuid:uid>/', PostDeleteView.as_view(), name='post-delete'),
]
