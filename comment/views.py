from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment

# ViewSet for handling comments
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter comments by post_id if provided in the URL."""
        post_id = self.kwargs.get('post_id')  # Using 'post_id' for clarity
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):

        """Override to set the author of the comment to the currently authenticated user.
          and also linked to the specified post"""
        post_id = self.kwargs.get('post_id')

        if not post_id:
            raise ValidationError("A post id is required to create a comment.")
        
        #request.data contains the data sent by the client, get serializer expects the data to be passed as a keyword argument which data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, post_id=post_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
