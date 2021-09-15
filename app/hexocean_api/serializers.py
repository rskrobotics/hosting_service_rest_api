from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class LinkSerializer(serializers.ModelSerializer):
    '''Serializer for Links'''

    def validate(self, data):
        if data['duration']:
            if data['duration'] < 300 or data['duration'] > 30000:
                raise serializers.ValidationError(
                    "Duration not blank or in range")
        return data

    class Meta:
        model = models.Link
        fields = ('thumbnail', 'duration')


class ThumbnailSerializer(serializers.ModelSerializer):
    '''Serializer for Thumbnails'''

    class Meta:
        model = models.Thumbnail
        fields = "__all__"


class BaseImageSerializer(serializers.ModelSerializer):
    '''Serializer for BaseImage'''

    class Meta:
        model = models.BaseImage
        fields = ('id', 'user', 'name', 'image')


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the Users object'''

    class Meta:
        model = get_user_model()
        fields = ('id', 'is_superuser', 'email', 'name', 'is_staff',
                  'account_plan')

    def create(self, validated_data):
        '''Create a new user with encrypted password and return it'''
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Update a user, setting the password correctly and return it'''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AccountPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountPlan
        fields = "__all__"
