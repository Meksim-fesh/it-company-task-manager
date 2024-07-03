from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Worker


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.select_related("position"),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateField(
        widget=forms.DateInput(format="%m/%d/%Y"),
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskFilterForm(forms.Form):

    TASK_COMPLETION_CHOICES = [
        ("all", "All"),
        (False, "Not completed"),
        (True, "Completed"),
    ]

    name = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )
    task_completion = forms.ChoiceField(
        choices=TASK_COMPLETION_CHOICES,
        initial=TASK_COMPLETION_CHOICES[0],
        label="Completion",
    )


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )
