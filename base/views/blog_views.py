from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from base.serializers import BlogSerializer, BlogsSerializer, CreateCommentSerializer
from base.models import Blog, Comment

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    # if blog.likes.filter(id=request.user.id):
    #     blog.liked = True
    # else:
    #     blog.liked = False
    serializer = BlogSerializer(blog,context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlogs(request):
    blogs = Blog.objects.filter(is_approved=True)
    new_blogs = blogs
    # for blog in blogs:
    #     if blog.likes.filter(id=request.user.id):
    #         blog.liked = True
    #         new_blogs.append(blog)
    #     else:
    #         blog.liked = False
    #         new_blogs.append(blog)
    serializer = BlogsSerializer(new_blogs,many = True,context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postBlog(request):
    serializer=BlogSerializer(data=request.data, remove_fields=['user','comment'])
    if serializer.is_valid():
        title = serializer.validated_data["title"]
        content = serializer.validated_data["content"]
        blog = Blog()
        blog.title = title
        blog.content = content
        blog.user = request.user
        blog.save()
        return Response(BlogSerializer(blog).data)
    else:
        return Response(serializer.errors)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postComment(request):
    serializer=CreateCommentSerializer(data=request.data, remove_fields=['user'])
    if serializer.is_valid():
        comment_data = serializer.validated_data["comment"]
        blog = serializer.validated_data["blog"]
        comment = Comment()
        comment.comment = comment_data
        comment.blog = blog
        comment.user = request.user
        comment.save()
        return Response({"message":"success"})
    else:
        return Response(serializer.errors)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likePost(request,pk):
    blog = Blog.objects.get(id=pk)
    liked = False
    if blog.likes.filter(id=request.user.id):
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True
    return Response({"message":liked })