from django import forms
from django.contrib.auth import get_user_model

from .models import Task


User = get_user_model()


class TaskCreateForm(forms.ModelForm):
    executors = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Executors",
    )

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "priority",
            "deadline",
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # ❌ запретить выбирать себя исполнителем
            self.fields["executors"].queryset = User.objects.exclude(id=user.id)