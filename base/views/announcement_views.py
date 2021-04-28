from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.serializers import AnnouncementSerializer

from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAnnouncements(request):
    announcements = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcements,many = True)
    return Response(serializer.data)