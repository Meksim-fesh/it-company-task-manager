from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from task_manager.forms import WorkerForm, WorkerUpdateForm

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


class PositionCreateView(generic.CreateView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
    fields = "__all__"


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 5


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position").prefetch_related(
        "tasks"
    )


class WorkerCreateView(generic.CreateView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")
    form_class = WorkerForm


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")
