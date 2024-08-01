from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.models import Task, TaskType, Position


class AdminPanelTest(TestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
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

    def test_position_list_display(self) -> None:
        url = reverse("admin:task_manager_position_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.position.name,)

    def test_position_detail_display(self) -> None:
        url = reverse(
            "admin:task_manager_position_change",
            args=[self.position.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.position.name,)

    def test_task_type_list_display(self) -> None:
        url = reverse("admin:task_manager_tasktype_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.tasktype.name,)

    def test_task_type_detail_display(self) -> None:
        url = reverse(
            "admin:task_manager_tasktype_change",
            args=[self.tasktype.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.tasktype.name,)

    def test_task_list_display(self) -> None:
        url = reverse("admin:task_manager_task_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.task.name,)

    def test_task_detail_display(self) -> None:
        url = reverse(
            "admin:task_manager_task_change",
            args=[self.task.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.task.name,)

    def test_worker_list_display(self) -> None:
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_display(self) -> None:
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id],
        )
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)
