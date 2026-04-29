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

def create_task(request):
    title = ''
    description = ''
    expiration_date = ''

    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        expiration_date = request.POST.get('expiration_date', '')

        if title and description and expiration_date:
            Task.objects.create(
                title=title,
                description=description,
                expiration_date=expiration_date
            )
            return redirect("create_task")  # or another success URL

    return render(request, 'create_task.html', {
        'title': title,
        'description': description,
        'expiration_date': expiration_date
    })