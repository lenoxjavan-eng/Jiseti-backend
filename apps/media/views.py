from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.records.models import Record

from .models import Media
from .serializers import MediaSerializer
from .services import create_media, delete_media


class RecordMediaListCreateView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def get(self, request, record_id):
		record = get_object_or_404(Record, pk=record_id)
		serializer = MediaSerializer(record.media.all(), many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, record_id):
		record = get_object_or_404(Record, pk=record_id)
		serializer = MediaSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		media = create_media(record=record, uploaded_file=serializer.validated_data['file'], media_type=serializer.validated_data['media_type'])
		return Response(MediaSerializer(media, context={'request': request}).data, status=status.HTTP_201_CREATED)


class MediaDeleteView(APIView):
	def delete(self, request, pk):
		media = get_object_or_404(Media, pk=pk)
		delete_media(media)
		return Response(status=status.HTTP_204_NO_CONTENT)
