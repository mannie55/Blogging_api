from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

CustomUser = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        # Validate password strength
        validate_password(password)

        return data


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        """
        Here we unpacked the validated_data dictionary and 
        converted them into keyword arguments
        """
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must provide both username and password")
            
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data




class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'birthdate']
        extra_kwargs = {
            'username': {'read_only':True}
        }