from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("id", "session_id", "result", "created_at", "user")
    list_filter = ("result", "created_at")
    search_fields = ("session_id", "result", "user__email", "user__full_name")
    readonly_fields = ("created_at",)
