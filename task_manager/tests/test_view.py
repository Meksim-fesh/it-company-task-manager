from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.models import Task, TaskType, Position


POSITION_LIST_URL = reverse("task_manager:position-list")
POSITION_CREATE_URL = reverse("task_manager:position-create")
POSITION_UPDATE_URL_STR = "task_manager:position-update"
POSITION_DELETE_URL_STR = "task_manager:position-delete"

TASK_TYPE_LIST_URL = reverse("task_manager:task_type-list")
TASK_TYPE_CREATE_URL = reverse("task_manager:task_type-create")
TASK_TYPE_UPDATE_URL_STR = "task_manager:task_type-update"
TASK_TYPE_DELETE_URL_STR = "task_manager:task_type-delete"

TASK_LIST_URL = reverse("task_manager:task-list")
TASK_CREATE_URL = reverse("task_manager:task-create")
TASK_DETAIL_URL_STR = "task_manager:task-detail"
TASK_UPDATE_URL_STR = "task_manager:task-update"
TASK_DELETE_URL_STR = "task_manager:task-delete"
TASK_TOGGLE_TASK_ASSIGN_URL_STR = "task_manager:toggle-task-assign"

WORKER_LIST_URL = reverse("task_manager:worker-list")
WORKER_CREATE_URL = reverse("task_manager:worker-create")
WORKER_DETAIL_URL_STR = "task_manager:worker-detail"
WORKER_UPDATE_URL_STR = "task_manager:worker-update"
WORKER_DELETE_URL_STR = "task_manager:worker-delete"


class PublicPositionViewTest(TestCase):

    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Test position"
        )

    def test_position_list_login_required(self) -> None:
        response = self.client.get(POSITION_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_position_create_login_required(self) -> None:
        response = self.client.get(POSITION_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_position_update_login_required(self) -> None:
        url = reverse(
            POSITION_UPDATE_URL_STR,
            args=(self.position.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_position_delete_login_required(self) -> None:
        url = reverse(
            POSITION_DELETE_URL_STR,
            args=(self.position.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.position_names_search = [
            "",
            "Designer",
            "er",
            "te",
            "e",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_positions(self) -> None:
        positions = [
            ("Designer"),
            ("Programmer"),
            ("Team Lead"),
            ("Tester"),
        ]
        for name in positions:
            Position.objects.create(
                name=name,
            )

    def test_retrieving_positions_list(self) -> None:
        self.creating_positions()
        response = self.client.get(POSITION_LIST_URL)
        position_list = Position.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(position_list)
        )
        self.assertTemplateUsed(
            response, "task_manager/position_list.html"
        )

    def test_position_search_result(self) -> None:
        self.creating_positions()
        for position_name in self.position_names_search:
            with self.subTest(position_name):
                response = self.client.get(
                    POSITION_LIST_URL,
                    {"name": position_name}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["position_list"]),
                    list(
                        Position.objects.filter(
                            name__icontains=position_name
                        )
                    )
                )

    def test_position_create(self) -> None:
        test_name = "Test position"
        response = self.client.post(
            POSITION_CREATE_URL,
            {
                "name": test_name,
            }
        )
        self.assertRedirects(response, POSITION_LIST_URL)
        position = Position.objects.get(name=test_name)
        self.assertEqual(position.name, test_name)

    def test_position_update(self) -> None:
        updated_name = "New name"
        self.position = Position.objects.create(
            name="Wrong name",
        )
        url = reverse(
            POSITION_UPDATE_URL_STR,
            args=[self.position.id, ]
        )
        response = self.client.post(
            url,
            {
                "name": updated_name,
            }
        )
        self.position.refresh_from_db()
        self.assertRedirects(response, POSITION_LIST_URL)
        self.assertEqual(self.position.name, updated_name)

    def test_position_delete(self) -> None:
        self.position = Position.objects.create(
            name="Test name",
        )
        url = reverse(
            POSITION_DELETE_URL_STR,
            args=[self.position.id, ]
        )
        response = self.client.post(url)
        self.assertRedirects(response, POSITION_LIST_URL)
        self.assertFalse(list(Position.objects.all()))


class PublicTaskTypeViewTest(TestCase):

    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="Test task type"
        )

    def test_task_type_list_login_required(self) -> None:
        response = self.client.get(TASK_TYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self) -> None:
        response = self.client.get(TASK_TYPE_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_update_login_required(self) -> None:
        url = reverse(
            TASK_TYPE_UPDATE_URL_STR,
            args=(self.task_type.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_delete_login_required(self) -> None:
        url = reverse(
            TASK_TYPE_DELETE_URL_STR,
            args=(self.task_type.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.task_type_names_search = [
            "",
            "Improvement",
            "re",
            "im",
            "e",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_task_types(self) -> None:
        task_types = [
            ("Refactoring"),
            ("New feature"),
            ("Bug fix"),
            ("Improvement"),
        ]
        for name in task_types:
            TaskType.objects.create(
                name=name,
            )

    def test_retrieving_task_types_list(self) -> None:
        self.creating_task_types()
        response = self.client.get(TASK_TYPE_LIST_URL)
        task_types_list = TaskType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types_list)
        )
        self.assertTemplateUsed(
            response, "task_manager/task_type_list.html"
        )

    def test_task_type_search_result(self) -> None:
        self.creating_task_types()
        for task_type_name in self.task_type_names_search:
            with self.subTest(task_type_name):
                response = self.client.get(
                    TASK_TYPE_LIST_URL,
                    {"name": task_type_name}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["task_type_list"]),
                    list(
                        TaskType.objects.filter(
                            name__icontains=task_type_name
                        )
                    )
                )

    def test_task_type_create(self) -> None:
        test_name = "Test task type"
        response = self.client.post(
            TASK_TYPE_CREATE_URL,
            {
                "name": test_name,
            }
        )
        self.assertRedirects(response, TASK_TYPE_LIST_URL)
        task_type = TaskType.objects.get(name=test_name)
        self.assertEqual(task_type.name, test_name)

    def test_task_type_update(self) -> None:
        updated_name = "New name"
        self.task_type = TaskType.objects.create(
            name="Wrong name",
        )
        url = reverse(
            TASK_TYPE_UPDATE_URL_STR,
            args=[self.task_type.id, ]
        )
        response = self.client.post(
            url,
            {
                "name": updated_name,
            }
        )
        self.task_type.refresh_from_db()
        self.assertRedirects(response, TASK_TYPE_LIST_URL)
        self.assertEqual(self.task_type.name, updated_name)

    def test_task_type_delete(self) -> None:
        self.task_type = TaskType.objects.create(
            name="Test name",
        )
        url = reverse(
            TASK_TYPE_DELETE_URL_STR,
            args=[self.task_type.id, ]
        )
        response = self.client.post(url)
        self.assertRedirects(response, TASK_TYPE_LIST_URL)
        self.assertFalse(list(TaskType.objects.all()))


class PublicTaskViewTest(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="Test name",
        )
        self.task = Task.objects.create(
            name="Test name",
            description="Test description",
            deadline="2006-06-06",
            is_completed=True,
            priority=Task.PRIORITY_CHOICES["URGENT"],
            task_type=self.task_type,
        )

    def test_task_list_login_required(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_create_login_required(self) -> None:
        response = self.client.get(TASK_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_detail_login_required(self) -> None:
        url = reverse(TASK_DETAIL_URL_STR, args=(self.task.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_task_update_login_required(self) -> None:
        url = reverse(TASK_UPDATE_URL_STR, args=(self.task.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_login_required(self) -> None:
        url = reverse(TASK_DELETE_URL_STR, args=(self.task.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_toggle_task_assign_login_required(self) -> None:
        url = reverse(TASK_TOGGLE_TASK_ASSIGN_URL_STR, args=(self.task.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.task_names_search = [
            "",
            "Add",
            "fix",
            "a",
            "guest",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_task_types_and_tasks(self) -> None:
        self.position = Position.objects.create(
            name="Developer"
        )
        self.user = get_user_model().objects.create_user(
            username="test.worker",
            password="1qazcde3",
            first_name="Bob",
            last_name="Rookie",
            position=self.position
        )
        self.new_feature = TaskType.objects.create(
            name="New feature",
        )
        self.bug = TaskType.objects.create(
            name="Bug",
        )
        tasks = [
            {
                "name": "Add an opportunity to log in as a guest",
                "description": "Short description",
                "deadline": "2024-09-09",
                "is_completed": False,
                "priority": Task.PRIORITY_CHOICES["HIGHT"],
                "task_type": self.new_feature,
                "assignees": [self.user.id, ]
            },
            {
                "name": "Add an opportunity to see changes were made",
                "description": "Short description",
                "deadline": "2024-10-10",
                "is_completed": False,
                "priority": Task.PRIORITY_CHOICES["MEDIUM"],
                "task_type": self.new_feature,
                "assignees": [self.user.id, ]
            },
            {
                "name": "Fix a bug when names were sorted wrong",
                "description": "Short description",
                "deadline": "2024-04-04",
                "is_completed": True,
                "priority": Task.PRIORITY_CHOICES["HIGHT"],
                "task_type": self.bug,
                "assignees": [self.user.id, ]
            },
            {
                "name": "Fix a bug when some people cant log in",
                "description": "Short description",
                "deadline": "2023-09-09",
                "is_completed": True,
                "priority": Task.PRIORITY_CHOICES["MEDIUM"],
                "task_type": self.bug,
                "assignees": [self.user.id, ]
            },
        ]
        for task_info in tasks:
            task = Task.objects.create(
                name=task_info["name"],
                description=task_info["description"],
                deadline=task_info["deadline"],
                is_completed=task_info["is_completed"],
                priority=task_info["priority"],
                task_type=task_info["task_type"],
            )
            task.assignees.set(task_info["assignees"])

    def test_retrieving_task_list(self) -> None:
        self.creating_task_types_and_tasks()
        response = self.client.get(TASK_LIST_URL)
        task_list = Task.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(task_list)
        )
        self.assertTemplateUsed(
            response, "task_manager/task_list.html"
        )

    def test_task_search_result(self) -> None:
        self.creating_task_types_and_tasks()
        for task_name in self.task_names_search:
            with self.subTest(task_name):
                response = self.client.get(
                    TASK_LIST_URL,
                    {"name": task_name}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["task_list"]),
                    list(
                        Task.objects.filter(
                            name__icontains=task_name
                        )
                    )
                )

    def test_task_create(self) -> None:
        test_task_name = "Test name"
        self.task_type = TaskType.objects.create(
            name="Test name",
        )
        self.position = Position.objects.create(
            name="Test name"
        )
        self.user = get_user_model().objects.create_user(
            username="test.worker",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            position=self.position
        )
        response = self.client.post(
            TASK_CREATE_URL,
            {
                "name": test_task_name,
                "description": "Test description",
                "deadline": "06/23/2024",
                "is_completed": True,
                "priority": "URGENT",
                "task_type": self.task_type.id,
                "assignees": [self.user.id, ],
            }
        )
        self.task = Task.objects.get(name=test_task_name)
        self.assertRedirects(response, TASK_LIST_URL)
        self.assertEqual(self.task.name, test_task_name)
        self.assertEqual(self.task.task_type, self.task_type)
        self.assertEqual(
            list(self.task.assignees.all()),
            [self.user]
        )

    def test_task_update(self) -> None:
        old_task_name = "Old name"
        new_task_name = "New name"
        self.task_type = TaskType.objects.create(
            name="Test name",
        )
        self.position = Position.objects.create(
            name="Test name"
        )
        self.user = get_user_model().objects.create_user(
            username="test.worker",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            position=self.position
        )
        self.task = Task.objects.create(
                name=old_task_name,
                description="Test description",
                deadline="2023-09-09",
                is_completed=True,
                priority=Task.PRIORITY_CHOICES["HIGHT"],
                task_type=self.task_type,
        )
        self.task.assignees.set([self.user, ])
        url = reverse(TASK_UPDATE_URL_STR, args=[self.task.id, ])
        response = self.client.post(
            url,
            {
                "name": new_task_name,
                "description": "Test description",
                "deadline": "09/09/2023",
                "is_completed": True,
                "priority": "HIGHT",
                "task_type": self.task_type.id,
                "assignees": [self.user.id, ],
            }
        )
        self.task.refresh_from_db()
        self.assertRedirects(response, TASK_LIST_URL)
        self.assertEqual(self.task.name, new_task_name)

    def test_retrieving_task_detail(self) -> None:
        self.creating_task_types_and_tasks()
        self.tasks = Task.objects.all()
        for task in self.tasks:
            with self.subTest(task):
                url = reverse(TASK_DETAIL_URL_STR, args=[task.id, ])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, task.name)
                self.assertContains(response, task.task_type.name)
                self.assertContains(response, task.description)
                self.assertContains(response, task.is_completed)

    def test_toggle_task_assign(self) -> None:
        self.task_type = TaskType.objects.create(
            name="Test name",
        )
        self.position = Position.objects.create(
            name="Test name"
        )
        self.user = get_user_model().objects.create_user(
            username="worker",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            position=self.position,
        )
        self.task = Task.objects.create(
                name="Test name",
                description="Test description",
                deadline="2023-09-09",
                is_completed=True,
                priority=Task.PRIORITY_CHOICES["HIGHT"],
                task_type=self.task_type,
        )
        self.task.assignees.set([self.user, ])
        url = reverse(TASK_TOGGLE_TASK_ASSIGN_URL_STR, args=[self.task.id, ])
        self.client.get(url)
        self.assignees = self.task.assignees.all()
        self.assertEqual(
            list(self.assignees),
            list(self.task.assignees.all())
        )
        self.client.get(url)
        self.assertNotEqual(
            list(self.assignees),
            list(self.task.assignees.all())
        )


class PublicWorkerViewTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Test name"
        )
        self.user = get_user_model().objects.create_user(
            username="test.worker",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            position=self.position,
        )

    def test_worker_list_login_required(self) -> None:
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_login_required(self) -> None:
        response = self.client.get(WORKER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_detail_login_required(self) -> None:
        url = reverse(WORKER_DETAIL_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_login_required(self) -> None:
        url = reverse(WORKER_UPDATE_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_delete_login_required(self) -> None:
        url = reverse(WORKER_DELETE_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.usernames_search = [
            "",
            "admin",
            "BOB",
            "eR",
            "b",
        ]

    def setUp(self) -> None:
        position = Position.objects.create(
            name="Admin",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
            position=position,
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_users(self) -> None:
        self.position = Position.objects.create(
            name="Test name"
        )
        users = [
            ("Bob", "1qazcde3", "Bob", "Cage", self.position),
            ("bruce.designer", "1qazcde3", "Bruce", "Dove", self.position),
            ("super.tester", "1qazcde3", "Super", "Driver", self.position),
            ("best-admin", "1qazcde3", "Admin", "Real", self.position),
        ]
        for username, password, first_name, last_name, position in users:
            get_user_model().objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                position=position,
            )

    def test_retrieving_worker_list(self) -> None:
        self.creating_users()
        response = self.client.get(WORKER_LIST_URL)
        worker_list = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(worker_list)
        )
        self.assertTemplateUsed(
            response, "task_manager/worker_list.html"
        )

    def test_worker_search_result(self) -> None:
        self.creating_users()
        for username in self.usernames_search:
            with self.subTest(username):
                response = self.client.get(
                    WORKER_LIST_URL,
                    {"username": username}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["worker_list"]),
                    list(
                        get_user_model().objects.filter(
                            username__icontains=username
                        )
                    )
                )

    def test_worker_detail(self) -> None:
        self.creating_users()
        self.users = get_user_model().objects.select_related("position")
        for user in self.users:
            with self.subTest(user):
                url = reverse(WORKER_DETAIL_URL_STR, args=[user.id, ])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, user.username)
                self.assertContains(response, user.first_name)
                self.assertContains(response, user.last_name)
                self.assertContains(response, user.position.name)

    def test_worker_create(self) -> None:
        username = "test.user"
        password = "1qazcde3"
        first_name = "Test_first"
        last_name = "Test_last"
        self.position = Position.objects.create(
            name="Test name"
        )
        response = self.client.post(
            WORKER_CREATE_URL,
            {
                "username": username,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "position": self.position.id,
            }
        )
        user = get_user_model().objects.get(username=username)
        self.assertRedirects(response, WORKER_LIST_URL)
        self.assertEqual(user.username, username)

    def test_worker_delete(self) -> None:
        self.position = Position.objects.create(
            name="Test name"
        )
        self.user = get_user_model().objects.create_user(
            username="test.worker",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            position=self.position,
        )
        self.user.save()
        url = reverse(WORKER_DELETE_URL_STR, args=[self.user.id, ])
        response = self.client.post(url)
        self.assertRedirects(response, WORKER_LIST_URL)
        self.assertFalse(len(list(get_user_model().objects.all())) >= 2)

    def test_worker_update(self) -> None:
        old_username = "test.user"
        new_username = "super.user"
        password = "1qazcde3"
        first_name = "Test_first"
        last_name = "Test_last"
        self.position = Position.objects.create(
            name="Test name",
        )
        self.user = get_user_model().objects.create_user(
            username=old_username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            position=self.position,
        )
        url = reverse(WORKER_UPDATE_URL_STR, args=[self.user.id, ])
        response = self.client.post(
            url,
            {
                "username": new_username,
                "first_name": first_name,
                "last_name": last_name,
                "position": self.position.id,
            }
        )
        self.user.refresh_from_db()
        self.assertRedirects(response, WORKER_LIST_URL)
        self.assertEqual(self.user.username, new_username)
