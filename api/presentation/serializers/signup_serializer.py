from django.contrib.auth.models import User
from rest_framework import serializers

from infrastructure import repositories
from infrastructure import model

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    # TODO:
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password didn't match."})
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        # repositories.CalendarRepository.create(self, user=user, name='Default')
        model.Calendar(user=user, name='Default').save()
        return user