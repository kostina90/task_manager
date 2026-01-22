from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    STATUS_AWAITING_APPOINTMENT = "awaiting_appointment"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_REVIEW = "review"
    STATUS_DONE = "done"
    STATUS_CANCELED = "canceled"

    TASK_STATUS_CHOICES = (
        (STATUS_AWAITING_APPOINTMENT, "Awaiting appointment"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_REVIEW, "Review"),
        (STATUS_DONE, "Done"),
        (STATUS_CANCELED, "Canceled")
    )

    LOW_PRIORITY = "low"
    MEDIUM_PRIORITY = "medium"
    HIGH_PRIORITY = "high"
    CRITICAL_PRIORITY = "critical"

    PRIORITY_CHOICES = (
        (LOW_PRIORITY, "Low"),
        (MEDIUM_PRIORITY, "Medium"),
        (HIGH_PRIORITY, "High"),
        (CRITICAL_PRIORITY, "Critical")
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=TASK_STATUS_CHOICES, default=STATUS_AWAITING_APPOINTMENT)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default=MEDIUM_PRIORITY)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_overdue(self):
        return (
            self.deadline and self.deadline < now() and self.status not in {self.STATUS_DONE, self.STATUS_CANCELED}
        )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["priority"])
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    

class TaskExecution(models.Model):
    STATUS_ASSIGNED = "assigned"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_REJECTED = "rejected"

    EXECUTION_STATUS_CHOICES = (
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_DONE, "Done"),
        (STATUS_REJECTED, "Rejected")
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="executions")
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=EXECUTION_STATUS_CHOICES, default=STATUS_ASSIGNED)
    comment = models.TextField(max_length=500, blank=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "executor"],
                name="unique_task_executor"
            )
        ]

    def __str__(self):
        return f"{self.task.title} - {self.executor.username}"
