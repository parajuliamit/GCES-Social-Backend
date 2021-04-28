from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from base.serializers import BlogSerializer, BlogsSerializer
from base.models import Blog

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlogs(request):
    blogs = Blog.objects.filter(is_approved=True)
    serializer = BlogsSerializer(blogs,many = True)
    return Response(serializer.data)
