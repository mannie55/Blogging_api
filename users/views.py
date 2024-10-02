from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from blog.permissions import IsAuthorOrReadOnly




CustomUser = get_user_model()



class RegistrationView(APIView):
    """
    API View for user registration.
    Handles the registration of a new user and returns a custom JSON response.
    """

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'bio': user.bio,
                    'birthdate': user.birthdate,
                },},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class LoginView(APIView):
    """API View for user login
    returns refresh and access token
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


    def get(self, request):
        """Retrieve the authenticated user's details."""
        user = request.user  
        serializer = UserSerializer(user)  
        return Response(serializer.data)
