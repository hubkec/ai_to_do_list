from ..models import Task

def handle_action(data, user):
    action = data.get("action")
    title = data.get("title")

    if action == "create":
        task = Task.objects.create(
            title=title or "Senza titolo",
            author=user   # 👈 FIX QUI
        )
        return f"Creato: {task.title}"

    return "Non ho capito"