from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from base.serializers import BatchSerializer, RoutineSerializer
from base.models import Batch, Routine, Subject

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutine(request,pk):
    # routine = Batch.objects.get(name = pk)
    # serializer = BatchSerializer(routine)
    serializer = RoutineSerializer(Routine.objects.all(),many = True,context={'batch': pk})
    return Response(serializer.data)