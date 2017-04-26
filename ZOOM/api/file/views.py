from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import api_view

from file_upload.models import File, FileSource, FileTag
from indicator.models import IndicatorDatapoint
from api.file.serializers import FileSerializer, FileSourceSerializer, FileTagSerializer
import os

@api_view(['POST'])
def delete_file(request):
    print("In delete file")
    file_id = request.data.get('file_id')
    print(file_id)
    
    instance = File.objects.get(id=request.data['file_id'])
    #FileSource.objects.get()
    #FileTag.objects.get()
    print instance
    indicator_instance = IndicatorDatapoint.objects.filter(file=instance)
    if indicator_instance:
        #indicator_instance = IndicatorDatapoint.objects.get(file=instance)
        print(len(indicator_instance))
        indicator_instance.delete()
    file = instance.file
    print(file)
    os.remove(str(file))
    instance.delete()
    return Response({"success": 1})


class FileListView(ListCreateAPIView):

    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser,)

    fields = (
        'id',
        'title',
        'description',
        'file',
        'file_name',
        'in_progress',
        'source_url',
        'data_source',
        'tags',
        'created',
        'modified',
        'rendered')

    def perform_create(self, serializer):
        serializer.save(
            file=self.request.data.get('file'), 
            file_name=self.request.data.get('file_name')
        )

    #def delete(self, request): getting front end error, permission denied for delete method 
    #    print("In self")


class FileDetailView(RetrieveUpdateDestroyAPIView):

    queryset = File.objects.all()
    serializer_class = FileSerializer   


class FileSourceListView(ListAPIView):

    queryset = FileSource.objects.all()
    serializer_class = FileSourceSerializer


class FileTagListView(ListCreateAPIView):

    queryset = FileTag.objects.all()
    serializer_class = FileTagSerializer

    def get_queryset(self):
        return self.queryset.filter(file_id=self.kwargs.get('file_source_pk'))

    def perform_create(self, serializer):
        file_id = get_object_or_404(
            FileSource, pk = self.kwargs.get('file_source_pk'))
        serializer.save(file_id=file_id)
