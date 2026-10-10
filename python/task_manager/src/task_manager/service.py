"""Application services for the task manager."""

from dataclasses import replace

from .exceptions import InvalidTaskError
from .models import Task
from .repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository: TaskRepository = repository

    def create_task(self, task_id: int, title: str) -> Task:
        self._validate_id(task_id)
        validated_title = self._validate_title(title)
        task = Task(task_id, validated_title)
        self._repository.add(task)
        return task

    def get_task(self, task_id: int) -> Task:
        self._validate_id(task_id)
        return self._repository.get(task_id)

    def list_tasks(self) -> list[Task]:
        return self._repository.get_all()

    def update_task(self, task_id: int, title: str) -> Task:
        self._validate_id(task_id)
        validated_title = self._validate_title(title)

        existing_task = self._repository.get(task_id)

        updated_task = replace(existing_task, title=validated_title)

        self._repository.update(updated_task)
        return updated_task

    def _validate_id(self, task_id: int) -> None:
        if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskError(
                f"Invalid task ID: {task_id!r}. ID must be a positive integer"
            )

    def _validate_title(self, title: str) -> str:
        if not isinstance(title, str):
            raise InvalidTaskError("Title must be a string.")
        normalized_title = title.strip()
        if not normalized_title:
            raise InvalidTaskError("Title should not be empty.")
        return normalized_title
