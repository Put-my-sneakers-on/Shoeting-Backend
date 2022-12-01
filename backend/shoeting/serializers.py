from rest_framework import serializers
from .models import *

class UserStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStyle
        fields = '__all__'