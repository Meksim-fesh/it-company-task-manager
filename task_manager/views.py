from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Worker, Position, TaskType, Task


def index(request: HttpRequest) -> HttpResponse:

    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_tasktypes = TaskType.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_tasktypes": num_tasktypes,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 5


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 5
