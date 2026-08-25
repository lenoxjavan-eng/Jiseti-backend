from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'type', 'status', 'user', 'created_at')
	list_filter = ('type', 'status', 'created_at')
	search_fields = ('title', 'description', 'user__username', 'user__email')
	readonly_fields = ('created_at', 'updated_at')
