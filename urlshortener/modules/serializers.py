from django.contrib.auth.models import User
from urlshortener.models import Urlshort
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class UrlshortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Urlshort
        fields = ('original_url', 'hash_value')