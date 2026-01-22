from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) | Q(executor=user)
        ).distinct()
    

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) | Q(executor=user)
        ).distinct()
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    fields = ("title", "description", "executor", "status", "deadline", "priority")
    success_url = reverse_lazy("tasks:tasks_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "tasks/task_update.html"
    fields = ("title", "description", "executor", "status", "deadline", "priority")
    
    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.pk})
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks:tasks_list")

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)
