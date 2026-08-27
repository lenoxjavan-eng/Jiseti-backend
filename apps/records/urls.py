from django.urls import path

from .views import AdminRecordStatusView, MyRecordListView, RecordDetailView, RecordListCreateView


urlpatterns = [
	path('admin/records/<int:pk>/status/', AdminRecordStatusView.as_view(), name='admin-record-status'),
	path('records/', RecordListCreateView.as_view(), name='record-list-create'),
	path('records/my-records/', MyRecordListView.as_view(), name='my-records'),
	path('records/<int:pk>/', RecordDetailView.as_view(), name='record-detail'),
]
