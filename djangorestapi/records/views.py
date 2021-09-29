from datetime import date
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from records.models import Record
from records.serializers import RecordSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def record_list(request):
    if request.method == 'GET':
        records = Record.objects.all()

        name = request.query_params.get('name', None)
        # if name is not None:
        if name:
            records = records.filter(name__icontains=name)
        
        records_serializer = RecordSerializer(records, many=True)
        return JsonResponse(records_serializer.data, safe=False)

    elif request.method == 'POST':
        record_data = JSONParser().parse(request)
        record_serializer = RecordSerializer(data=record_data)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse(record_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Record.objects.all().delete()
        return JsonResponse({'message': '{} Records were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def record_detail(request, pk):
    try:
        record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return JsonResponse({'message': 'The record does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        record_serializer = RecordSerializer(record)
        return JsonResponse(record_serializer.data)
    
    elif request.method == 'PUT':
        record_data = JSONParser().parse(request)
        record_serializer = RecordSerializer(record, data=record_data)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse(record_serializer.data)
        return JsonResponse(record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        record.delete()
        return JsonResponse({'message': 'Record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        