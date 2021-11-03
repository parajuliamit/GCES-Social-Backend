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
    user = serializers.CharField(source = "user.first_name" )
    class Meta:
        model = Comment
        fields = ["id","user","comment","createdAt"]

class CreateCommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(CreateCommentSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
                
    class Meta:
        model = Comment
        fields = '__all__'

class BlogsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    liked = serializers.SerializerMethodField(method_name='check_like')
    
    def check_like(self,obj):
        request = self.context.get("request")
        current_user = request.user
        print(current_user.id)
        if obj.likes.filter(id=current_user.id):
            return True
        else:
            return False

    class Meta:
        model = Blog
        fields =["id","user","title","createdAt","total_likes","comment_count","liked"]


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    comment = CommentSerializer(many=True, source="comment_set.all")
    liked = serializers.SerializerMethodField(method_name='check_like')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(BlogSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
    
    def check_like(self,obj):
        request = self.context.get("request")
        current_user = request.user
        print(current_user.id)
        if obj.likes.filter(id=current_user.id):
            return True
        else:
            return False
 
    class Meta:
        model = Blog
        fields = ["id","user","title","createdAt","total_likes","comment_count","content","comment","liked"]
    

