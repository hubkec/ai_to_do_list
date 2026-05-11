from ..models import Task

def handle_action(data, user):
    action = data.get("action")
    title = data.get("title")
    completed = data.get("completed")  # 👈 nuovo

    if action == "create":
        task = Task.objects.create(
            title=title or "Senza titolo",
            author=user
        )
        return f"Creato: {task.title}"

    elif action == "delete":
        if not title:
            return "Cosa devo cancellare?"

        tasks = Task.objects.filter(
            author=user,
            title__icontains=title
        )

        count = tasks.count()

        if count == 0:
            return "Nessun task trovato"

        tasks.delete()
        return f"Eliminati {count} task"

    elif action == "toggle":
        if not title:
            return "Quale task devo aggiornare?"

        tasks = Task.objects.filter(
            author=user,
            title__icontains=title
        )

        if not tasks.exists():
            return "Task non trovato"

        updated = 0

        for task in tasks:
            if completed is not None:
                task.completed = completed
            else:
                task.completed = not task.completed

            task.save()
            updated += 1

        return f"Aggiornati {updated} task"

    return "Non ho capito"