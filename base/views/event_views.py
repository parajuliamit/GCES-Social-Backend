from datetime import date, timedelta

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from base.serializers import EventSerializer
from base.models import Event

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEvents(request,pk):
    events =  Event.objects.filter(batch=pk) | Event.objects.filter(batch='All') 
    startdate = date.today()
    enddate = startdate + timedelta(days=365)
    serializer =  EventSerializer(events.filter(date__range=[startdate, enddate]),many = True)
    serializer_data = sorted(
            serializer.data, key=lambda k: k['date'])
    return Response(serializer_data)
