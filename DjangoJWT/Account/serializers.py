from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer

from .models import *

# Setting for using JWT
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# Load User Model
User = get_user_model()


# Register
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True, max_length=20)
    introduction = serializers.CharField(required=False, max_length=200)
    profile_image = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()  # Default Data
        data_dict['nickname'] = self.validated_data('nickname', '')
        data_dict['introduction'] = self.validated_data('introduction', '')
        data_dict['profile_image'] = self.validated_data('profile_image', '')

        return data_dict


# Login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {'username' : 'None'}

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )

        return {
            'username' : user.username,
            'token' : jwt_token
        }

# Load User Data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ('id', 'username', 'nickname', 'introduction', 'profile_image')