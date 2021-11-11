from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from base.serializers import AnnouncementSerializer
from base.models import Announcement

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllAnnouncements(request):
    announcements = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcements,many = True)
    serializer_data = sorted(
            serializer.data, key=lambda k: k['id'], reverse=True)
    return Response(serializer_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAnnouncements(request,pk):
    announcements =  Announcement.objects.filter(batch=pk) | Announcement.objects.filter(batch='All')
    serializer =  AnnouncementSerializer(announcements,many = True)
    serializer_data = sorted(
            serializer.data, key=lambda k: k['id'], reverse=True)
    return Response(serializer_data)
