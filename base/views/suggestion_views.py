from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from base.serializers import SuggestionSerializer
from base.models import Suggestion

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postSuggestion(request):
    serializer=SuggestionSerializer(data=request.data)
    if serializer.is_valid():
        suggestion = Suggestion()
        is_anonymous = serializer.validated_data["is_anonymous"]
        suggestion.content = serializer.validated_data["content"]
        if is_anonymous==False:
            suggestion.user = request.user
        suggestion.save()
        return Response({"message":"suggestion received."})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 