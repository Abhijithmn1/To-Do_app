from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import Todoform
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView,DeleteView


class Tasklist(ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "task"


class TaskDetail(DetailView):
    model = Task
    template_name = "detail.html"
    context_object_name = "task"


class TaskUpdate(UpdateView):
    model = Task
    template_name = "update.html"
    context_object_name = 'task'
    fields = ("name", "priority", "date")

    def get_success_url(self):
        return reverse_lazy('todo_app:cbvdetail', kwargs={'pk': self.object.id})



class TaskDelete(DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy('todo_app:cbvhome')


# Create your views here.
def add(request):
    view = Task.objects.all()
    if request.method == "POST":
        name = request.POST.get("task", '')
        priority = request.POST.get("priority", '')
        date = request.POST.get("date", '')
        task = Task(name=name, priority=priority, date=date)
        task.save()
    return render(request, "home.html", {"task": view})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == "POST":
        task.delete()
        return redirect("/")
    return render(request, "delete.html")


def update(request, id):
    task = Task.objects.get(id=id)
    fom = Todoform(request.POST or None, instance=task)
    if fom.is_valid():
        fom.save()
        return redirect('/')
    return render(request, 'edit.html', {'fom': fom, 'task': task})
