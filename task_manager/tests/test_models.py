from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.models import Task, TaskType, Position


class ModelTest(TestCase):

    def setUp(self) -> None:
        self.tasktype = TaskType.objects.create(
            name="Test type",
        )
        self.position = Position.objects.create(
            name="Test position",
        )
        self.worker = get_user_model().objects.create_user(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="Test name",
            description="Test description",
            deadline="2006-06-06",
            is_completed=True,
            priority=Task.PRIORITY_CHOICES["URGENT"],
            task_type=self.tasktype,
        )

    def test_task_str(self) -> None:
        deadline_str = f"Till: {self.task.deadline}"
        priority_str = f"priority: {self.task.priority}"
        brackets = f"({deadline_str}, {priority_str})"
        self.assertEqual(
            str(self.task),
            f"{self.task.name} {brackets}"
        )

    def test_position_str(self) -> None:
        self.assertEqual(
            str(self.position),
            self.position.name,
        )

    def test_task_type_str(self) -> None:
        self.assertEqual(
            str(self.tasktype),
            self.tasktype.name,
        )

    def test_worker_str(self) -> None:
        full_name_str = f"{self.worker.first_name} {self.worker.last_name}"
        self.assertEqual(
            str(self.worker),
            f"{self.worker.position} {full_name_str}"
        )
