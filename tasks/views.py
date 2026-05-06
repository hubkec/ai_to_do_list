from django.shortcuts import render, redirect
from .models import Task
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .services.ai_service import process_input
from .services.task_service import handle_action


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

        if title and description:
            Task.objects.create(
                author=request.user,
                title=title,
                description=description,
                expiration_date=expiration_date or None
            )
            return redirect("task_list")  

    return render(request, 'create_task.html', {
        'title': title,
        'description': description,
        'expiration_date': expiration_date
    })

def remove_task(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect('task_list')


def ai_view(request):
    user_input = request.GET.get("q")

    data = process_input(user_input)
    result = handle_action(data, request.user) 

    return JsonResponse({
        "result": result
    })