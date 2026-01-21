from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "deadline", "priority", "creator", "get_executors", "is_overdue", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "status", "priority")
    search_fields = ("title", "creator__username", "executor__username")
    readonly_fields = ("id", "creator", "is_overdue")
    list_per_page = 10

    fieldsets = (
        ("Main Info:", {
            "classes": ("wide",),
            "fields": ("title", "description", "executor"),
        }),
        ("Additional info", {
            "classes": ("wide",),
            "fields": ("status", "deadline", "priority", "is_overdue")
        })
    )

    def get_executors(self, obj):
        return ", ".join(user.username for user in obj.executor.all())
    
    get_executors.short_description = "Executors"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def is_overdue(self, obj):
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue"
