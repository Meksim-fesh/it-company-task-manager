from django.urls import path

import task_manager.views as views


urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "positions/",
        views.PositionListView.as_view(),
        name="position-list",
    ),
    path(
        "positions/create/",
        views.PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "positions/<int:pk>/update/",
        views.PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        views.PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path(
        "workers/",
        views.WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "workers/<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail",
    ),
    path(
        "workers/create/",
        views.WorkerCreateView.as_view(),
        name="worker-create",
    ),
    path(
        "workers/<int:pk>/update/",
        views.WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete/",
        views.WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "task_types/",
        views.TaskTypeListView.as_view(),
        name="task_type-list",
    ),
    path(
        "task_types/create/",
        views.TaskTypeCreateView.as_view(),
        name="task_type-create",
    ),
    path(
        "task_types/<int:pk>/update/",
        views.TaskTypeUpdateView.as_view(),
        name="task_type-update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        views.TaskTypeDeleteView.as_view(),
        name="task_type-delete",
    ),
    path(
        "tasks/",
        views.TaskListView.as_view(),
        name="task-list",
    ),
]

app_name = "task_manager"
