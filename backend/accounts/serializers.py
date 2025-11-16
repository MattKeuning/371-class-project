from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
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
        user_data = validated_data.get('user', {})
        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()

        return instance