from rest_framework import serializers
from .models import User
from api.core.models import ClientProfile, VolunteerProfile, PaymentHistory, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'role']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'role']
        extra_kwargs = {
            'role': {'read_only': True}
        }

