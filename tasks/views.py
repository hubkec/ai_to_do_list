from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    filter_param = request.GET.get('filter', 'all')

    if filter_param == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif filter_param == 'incomplete':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    return render(request, 'tasks.html', {'tasks': tasks, 'filter_param': filter_param})

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
                author=request.user,
                title=title,
                description=description,
                expiration_date=expiration_date
            )
            return redirect("task_list")  

    return render(request, 'create_task.html', {
        'title': title,
        'description': description,
        'expiration_date': expiration_date
    })