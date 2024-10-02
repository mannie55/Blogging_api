from rest_framework import serializers
from .models import BlogPost, Category
from django.contrib.auth import get_user_model
from taggit.serializers import TagListSerializerField, TaggitSerializer

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=User.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'title']




class BlogPostSerializer(TaggitSerializer, serializers.ModelSerializer):
  """
  slugrelated field to ensure api call returns author username instead of primarykey
  """
  author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

  # tags = TagListSerializerField()

  class Meta:
    model = BlogPost
    fields = '__all__'
    read_only_fields = ['author']