from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'name', 'age']

    def update(self, instance, validated_data):
        # Update UserProfile fields
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.save()

        # Update User email if provided
        if 'email' in validated_data:
            instance.user.email = validated_data['email']
            instance.user.save()

        return instance