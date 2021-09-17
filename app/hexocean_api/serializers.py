from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


class ExpiringLinkSerializer(serializers.ModelSerializer):
    '''Serializer for Links'''

    class Meta:
        model = models.Link
        fields = ('thumbnail', 'duration')

    def validate(self, data):
        if data['duration']:
            if data['duration'] < 300 or data['duration'] > 30000:
                raise serializers.ValidationError(
                    "Duration not blank or in range")
        return data


class LinkSerializer(serializers.ModelSerializer):
    '''Serializer for Links'''
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Link
        fields = ('thumbnail', 'duration', 'access_str', 'created_on', 'url')

    def validate(self, data):
        if data['duration']:
            if data['duration'] < 300 or data['duration'] > 30000:
                raise serializers.ValidationError(
                    "Duration not blank or in range")
        return data

    def get_url(self, obj):
        url_base = 'http://localhost:8000/images'
        full_url = f'{url_base}/{obj.access_str}'
        return full_url


class ThumbnailSerializer(serializers.ModelSerializer):
    '''Serializer for Thumbnails'''
    link = serializers.SerializerMethodField()

    class Meta:
        model = models.Thumbnail
        fields = ('base_image', 'height', 'name', 'link')

    def get_link(self, obj):
        result = models.Link.objects.filter(thumbnail=obj).distinct()
        return LinkSerializer(result, many=True).data


class BaseImageListSerializer(serializers.ModelSerializer):
    '''Serializer for BaseImage'''

    class Meta:
        model = models.BaseImage
        fields = ('id', 'user', 'name')
        read_only_fields = ('user',)


class BaseImageSerializer(serializers.ModelSerializer):
    '''Serializer for BaseImage'''

    class Meta:
        model = models.BaseImage
        fields = ('id', 'user', 'name', 'image')
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the Users object'''

    class Meta:
        model = get_user_model()
        fields = ('id', 'is_superuser', 'email', 'name', 'is_staff',
                  'account_plan')

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
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
