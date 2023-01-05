from rest_framework import serializers
from .models import *

class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        nickname = validated_data.get('nickname')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            user_id=user_id,
            nickname=nickname,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStyle
        fields = '__all__'