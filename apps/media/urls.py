from django.urls import path

from .views import MediaDeleteView, RecordMediaListCreateView


urlpatterns = [
	path('records/<int:record_id>/media/', RecordMediaListCreateView.as_view(), name='record-media'),
	path('media/<int:pk>/', MediaDeleteView.as_view(), name='media-delete'),
]
