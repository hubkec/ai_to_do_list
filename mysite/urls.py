"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls
from django.contrib import admin
from django.urls import path
from tasks.views import (
    task_list,
    task_detail,
    toggle_task,
    create_task,
    remove_task,
    ai_view,
    register,
    my_profile
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML views
    path('task/<int:id>', task_detail, name="task"),
    path('task/<int:id>/toggle/', toggle_task, name='toggle_task'),
    path('task/<int:id>/delete/', remove_task, name='remove_task'),
    path('ai/', ai_view),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # API

    path('api/profile/', my_profile, name="my_profile"),
    path('api/tasks/', task_list, name="task_list"),
    path('api/task/<int:id>', task_detail, name="task"),
    path('api/task/create/', create_task, name="create_task"),
    path('api/register/', register),
]