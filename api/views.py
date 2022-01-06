from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import TestModel
from api.serializers import TestSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def testView(request):
    if(request.method == 'GET'):
        tests = TestModel.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    if(request.method == 'POST'):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
