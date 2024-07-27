from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from task_manager.forms import (
    PositionNameSearchForm,
    TaskForm,
    TaskFilterForm,
    TaskTypeNameSearchForm,
    WorkerForm,
    WorkerUpdateForm,
    WorkerUsernameSearchForm,
)

from .models import Worker, Position, TaskType, Task


@login_required
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


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionNameSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PositionNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
    fields = "__all__"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username},
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerUsernameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position").prefetch_related(
        "tasks"
    )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")
    form_class = WorkerForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 6
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeNameSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskTypeNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task_type-list")
    template_name = "task_manager/task_type_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        task_completion = self.request.GET.get("task_completion", "all")
        order = self.request.GET.get("order", "none")
        context["filter_form"] = TaskFilterForm(
            initial={
                "name": name,
                "task_completion": task_completion,
                "order": order,
            },
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        queryset = self.filter_by_completion_status(queryset)
        queryset = self.filter_by_name(queryset)
        queryset = self.order_by(queryset)
        return queryset

    def filter_by_completion_status(self, queryset):
        completion_status = self.request.GET.get("task_completion", "all")
        if completion_status != "all":
            return queryset.filter(is_completed=completion_status)
        return queryset

    def filter_by_name(self, queryset):
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def order_by(self, queryset):
        order = self.request.GET.get("order", "none")
        if order != "none":
            return queryset.order_by(order)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees__position")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class ToggleAssignToTask(LoginRequiredMixin, generic.UpdateView):

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        worker = request.user
        task_id = request.POST.get("task_id")
        task = Task.objects.get(id=task_id)

        if worker in task.assignees.all():
            task.assignees.remove(worker)
        else:
            task.assignees.add(worker)
        return HttpResponseRedirect(
            reverse_lazy("task_manager:task-detail", args=[task_id])
        )
