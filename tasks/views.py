from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .services.ai_service import process_input
from .services.task_service import handle_action
from tasks.serializers import TaskSerializer


# def task_list(request):
#     filter_param = request.GET.get('filter', 'all')
#
#     if filter_param == 'completed':
#         tasks = Task.objects.filter(completed=True)
#     elif filter_param == 'incomplete':
#         tasks = Task.objects.filter(completed=False)
#     else:
#         tasks = Task.objects.all()
#
#     return render(request, 'tasks.html', {'tasks': tasks, 'filter_param': filter_param})

# def task_detail(request, id):
#     task = Task.objects.get(pk=id)
#     return render(request, "task.html", {"task": task})


def toggle_task(request, id):
    task = get_object_or_404(Task, pk=id, author=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task', id=id)


# def create_task(request):
#     title = ''
#     description = ''
#     expiration_date = ''
#
#     if request.method == 'POST':
#         title = request.POST.get('title', '')
#         description = request.POST.get('description', '')
#         expiration_date = request.POST.get('expiration_date', '')
#
#         if title and description:
#             Task.objects.create(
#                 author=request.user,
#                 title=title,
#                 description=description,
#                 expiration_date=expiration_date or None
#             )
#             return redirect("task_list")
#
#     return render(request, 'create_task.html', {
#         'title': title,
#         'description': description,
#         'expiration_date': expiration_date
#     })


def remove_task(request, id):
    task = get_object_or_404(Task, pk=id, author=request.user)
    task.delete()
    return redirect('task_list')


def ai_view(request):
    user_input = request.GET.get("q")
    user_input_lower = user_input.lower()

    data = process_input(user_input)

    if data.get("action") == "toggle" and data.get("completed") is None:
        if any(word in user_input_lower for word in ["completa", "fatto", "finito"]):
            data["completed"] = True
        elif any(word in user_input_lower for word in ["riapri", "non completato"]):
            data["completed"] = False

    result = handle_action(data, request.user)

    return JsonResponse({
        "result": result,
        "debug": data
    })


# -- API --
@api_view(["GET"])
def my_profile(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
    })


@api_view(["GET"])
def task_list(request):
    tasks = Task.objects.filter(author=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def task_detail(request, id):
    task = get_object_or_404(Task, pk=id, author=request.user)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def create_task(request):
    title = request.data.get("title")
    description = request.data.get("description")

    if not title or not description:
        return Response(
            {"error": "Missing fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    task = Task.objects.create(
        author=request.user,
        title=title,
        description=description
    )

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Missing fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    return Response({
        "id": user.id,
        "username": user.username
    }, status=status.HTTP_201_CREATED)