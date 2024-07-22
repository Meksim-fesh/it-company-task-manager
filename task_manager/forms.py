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
                "placeholder": "Search by username",
                "class": "text-white",
            }
        ),
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
    TASK_ORDER_BY_CHOICES = [
        ("none", "None"),
        ("name", "Name - from A to z"),
        ("-name", "Name - from z to A"),
        ("deadline", "Deadline - from closest"),
        ("-deadline", "Deadline - from farthest"),
    ]

    name = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "text-white",
            }
        ),
    )
    task_completion = forms.ChoiceField(
        choices=TASK_COMPLETION_CHOICES,
        initial=TASK_COMPLETION_CHOICES[0],
        label="",
        widget=forms.Select(
            attrs={
                "class": "text-white",
            }
        ),
    )
    order = forms.ChoiceField(
        choices=TASK_ORDER_BY_CHOICES,
        initial=TASK_ORDER_BY_CHOICES[0],
        label="",
        widget=forms.Select(
            attrs={
                "class": "text-white",
            }
        ),
    )


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=256,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": " text-white",
            }
        ),
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
        ),
    )
