from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Bb
from .models import Outfit


class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ('id', 'title', 'price', 'image', 'author', 'likes')


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', \
                    'image')
