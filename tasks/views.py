from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) | Q(executor=user)
        ).distinct()
    

class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) | Q(executor=user)
        ).distinct()
