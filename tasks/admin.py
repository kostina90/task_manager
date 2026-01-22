from django.contrib import admin

from .models import Task, TaskExecution


class TaskExecutionInline(admin.TabularInline):
    model = TaskExecution
    extra = 0
    autocomplete_fields = ("executor",)
    fields = ("executor", "status", "comment", "finished_at")
    readonly_fields = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "deadline",
        "priority",
        "creator",
        "executors_list",
        "is_overdue",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id", "title")
    list_filter = ("status", "priority", "created_at")
    search_fields = (
        "title",
        "creator__username",
        "executions__executor__username",
    )
    readonly_fields = ("id", "creator", "is_overdue", "created_at", "updated_at")
    list_per_page = 10

    inlines = (TaskExecutionInline,)

    fieldsets = (
        ("Main Info", {
            "fields": ("title", "description"),
        }),
        ("Additional Info", {
            "fields": ("status", "deadline", "priority", "is_overdue"),
        }),
        ("Meta", {
            "fields": ("creator", "created_at", "updated_at"),
        }),
    )

    def executors_list(self, obj):
        return ", ".join(
            execution.executor.username
            for execution in obj.executions.select_related("executor")
        )

    executors_list.short_description = "Executors"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def is_overdue(self, obj):
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue"


@admin.register(TaskExecution)
class TaskExecutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "executor",
        "status",
        "finished_at",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = (
        "task__title",
        "executor__username",
    )

    autocomplete_fields = ("task", "executor")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Execution Info", {
            "fields": ("task", "executor", "status"),
        }),
        ("Result", {
            "fields": ("comment", "finished_at"),
        }),
        ("Meta", {
            "fields": ("created_at",),
        }),
    )
