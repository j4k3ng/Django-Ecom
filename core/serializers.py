from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
