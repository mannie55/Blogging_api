from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
import uuid

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class BlogPost(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts",
        null=True, blank=True
    )
    tags = TaggableManager()

    def __str__(self):
        return self.title
