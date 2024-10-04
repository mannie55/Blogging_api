from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from blog.permissions import IsAuthorOrReadOnly




CustomUser = get_user_model()



class RegistrationView(CreateAPIView):
    """
    API View for user registration.
    Handles the registration of a new user and returns a custom JSON response.
    """
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'bio': user.bio,
                    'birthdate': user.birthdate,
                },
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class LoginView(GenericAPIView):
    """API View for user login
    Returns refresh and access token
    """
    
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return self._generate_tokens(user)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_tokens(self, user):
        """Generate refresh and access tokens for the user."""
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = UserSerializer

    def get_object(self):
        """Override to return the authenticated user."""
        return self.request.user
