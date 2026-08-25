from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RecordSerializer
from .services import create_record


class RecordListCreateView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		queryset = request.user.records.all()
		if request.user.is_staff:
			from .models import Record
			queryset = Record.objects.all()
		return Response(RecordSerializer(queryset, many=True, context={'request': request}).data)

	def post(self, request):
		serializer = RecordSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		record = create_record(user=request.user, **serializer.validated_data)
		return Response(RecordSerializer(record, context={'request': request}).data, status=status.HTTP_201_CREATED)
