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
        "workers/",
        views.WorkerListView.as_view(),
        name="worker-list",
    ),
]

app_name = "task_manager"
