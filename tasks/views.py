from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Task, TaskExecution
from .forms import TaskCreateForm


User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) |
            Q(executions__executor=user)
        ).distinct()
    

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) |
            Q(executions__executor=user)
        ).distinct()
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()

        executors = form.cleaned_data["executors"]
        for user in executors:
            TaskExecution.objects.create(
                task=task,
                executor=user
            )

        self.object = task   # 🔥 ВАЖНО
        return redirect(self.get_success_url())
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "tasks/task_update.html"
    fields = (
        "title",
        "description",
        "status",
        "deadline",
        "priority",
    )

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.pk}
        )
    

class TaskExecutionUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskExecution
    template_name = "tasks/task_executor_update.html"
    fields = ("executor",)

    def get_queryset(self):
        """
        Доступ ТОЛЬКО создателю задачи
        """
        return TaskExecution.objects.filter(
            task__creator=self.request.user
        ).select_related("task", "executor")

    def get_form(self, form_class=None):
        """
        Убираем создателя задачи из списка исполнителей
        """
        form = super().get_form(form_class)

        task_creator_id = self.object.task.creator_id

        form.fields["executor"].queryset = User.objects.exclude(
            id=task_creator_id
        )

        return form

    def form_valid(self, form):
        """
        Если сменили исполнителя — сбрасываем статус
        """
        if form.instance.executor != self.object.executor:
            form.instance.status = TaskExecution.STATUS_ASSIGNED
            form.instance.comment = ""
            form.instance.finished_at = None

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.pk}
        )
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)
