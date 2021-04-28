from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import *

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name']

    def get_name(self,obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name','token']

    def get_token(self,obj):
        token = AccessToken.for_user(obj)
        return str(token)

class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Announcement
        fields = '__all__'
    
    def get_user(self,obj):
        user = obj.user.first_name 
        if user == '':
            user = obj.user.email

        return user

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = Comment
        fields = ["id","user","comment","createdAt"]

class BlogsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = Blog
        fields =["id","user","title","createdAt","likes","comment_count",]


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    comment = CommentSerializer(many=True, source="comment_set.all")
    class Meta:
        model = Blog
        fields = ["id","user","title","createdAt","likes","comment_count","content","comment"]
