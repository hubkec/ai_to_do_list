from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})

def task_detail(request, id):
    task = Task.objects.get(pk= id)
    return render(request, "task.html", {"task": task})

def toggle_task(request, id):
    task = Task.objects.get(pk= id)
    task.completed = not task.completed
    task.save()
    return redirect('task', id=id)
