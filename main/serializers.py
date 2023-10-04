from rest_framework import serializers
from rest_framework import generics
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'uuid', 'bio', 'name']
        

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'start_date', 'title', 'description']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'type']


class UsersTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTag
        fields = ['id', 'user', 'tag']


class ProjectsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsTag
        fields = ['id', 'project', 'tag']


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


