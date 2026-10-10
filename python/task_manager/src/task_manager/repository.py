from .exceptions import DuplicateTaskError, TaskNotFoundError
from .models import Task


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}

    def add(self, task: Task) -> None:
        if task.id in self._tasks:
            raise DuplicateTaskError(f"A task with this id: {task.id} exists!")
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"There is no task with this id: {task_id}!")
        return self._tasks[task_id]

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task: Task) -> None:
        if task.id not in self._tasks:
            raise TaskNotFoundError(f"There is no task with this id: {task.id}")
        self._tasks[task.id] = task
