from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth.models import User

# Extend the djoser standard serializer to create a new user
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

# Extend the djoser standard serializer to display a user
class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',
                  'email', 'first_name', 'last_name']
