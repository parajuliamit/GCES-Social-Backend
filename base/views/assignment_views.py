from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers, status

from base.serializers import SubmitAssignmentSerializer, AssignmentsSerializer, AssignmentSerializer
from base.models import Assignment, AssignmentSubmission

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    serializer = AssignmentSerializer(assignment,context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAssignments(request,pk):
    assignments = Assignment.objects.filter(batch=pk) | Assignment.objects.filter(batch='All')
    serializer = AssignmentsSerializer(assignments,many = True,context={'request': request})
    serializer_data = sorted(
            serializer.data, key=lambda k: k['id'], reverse=True)
    return Response(serializer_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createAssignment(request):
    return Response({"response":"success"})
    # serializer = AssignmentSerializer(data=request.data, remove_fields=['user','comment'])
    # if serializer.is_valid():
    #     title = serializer.validated_data["title"]
    #     content = serializer.validated_data["content"]
    #     blog = Blog()
    #     blog.title = title
    #     blog.content = content
    #     blog.user = request.user
    #     blog.save()
    #     return Response(BlogSerializer(blog,context={'request': request}).data)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submitAssignment(request):
    serializer = SubmitAssignmentSerializer(data=request.data, remove_fields=['user'])
    if serializer.is_valid():
        file = serializer.validated_data["file"]
        assignment = serializer.validated_data["assignment"]
        submission = AssignmentSubmission()
        submission.file = file
        submission.assignment = assignment
        submission.user = request.user
        submission.save()
        return Response({"message":"success"})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def markAssignment(request,pk):
    submission = AssignmentSubmission.objects.get(id=pk)
    return Response({"response":"success"})