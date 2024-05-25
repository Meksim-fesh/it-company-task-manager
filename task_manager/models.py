from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return f"{self.position} {self.first_name} {self.last_name}"


class Task(models.Model):
    PRIORITY_CHOICES = {
        "URGENT": "Urgent",
        "HIGHT": "Hight",
        "MEDIUM": "Medium",
        "LOW": "Low",
    }

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=6)
    task_type = models.ForeignKey(
        TaskType,
        null=True,
        on_delete=models.SET_NULL,
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    
    def __str__(self) -> str:
        return f"{self.name} (Till: {self.deadline}, priority: {self.priority})"


