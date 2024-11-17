from django.db import models
from blog.models import BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    