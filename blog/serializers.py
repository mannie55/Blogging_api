from rest_framework import serializers
from .models import BlogPost, Category, Tag
from django.contrib.auth import get_user_model
from taggit.serializers import TagListSerializerField, TaggitSerializer

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Tag
      fields = ['id', 'name']



class BlogPostSerializer(TaggitSerializer, serializers.ModelSerializer):

  class Meta:
    model = BlogPost
    fields = ['title', 'content', 'author', 'category', 'tags']
    read_only_fields = ['author']
