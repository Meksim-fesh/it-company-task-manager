from django.urls import path

import task_manager.views as views


urlpatterns = [
    path("", views.index, name="index",),
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
]

app_name = "task_manager"
