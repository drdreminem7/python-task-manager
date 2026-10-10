import pytest

from task_manager.exceptions import DuplicateTaskError, TaskNotFoundError
from task_manager.models import Task, TaskStatus
from task_manager.repository import TaskRepository


def test_add_task() -> None:
    repository = TaskRepository()
    task = Task(1, "Learn Python")
    repository.add(task)
    assert repository.get(task.id) == task


def test_add_duplicate_task() -> None:
    repository = TaskRepository()
    original = Task(1, "Learn Python")
    duplicate = Task(1, "Learn SQL")

    repository.add(original)

    with pytest.raises(DuplicateTaskError):
        repository.add(duplicate)

    assert repository.get(1) == original
    assert len(repository.get_all()) == 1


def test_get_nonexistent_task() -> None:
    repository = TaskRepository()

    with pytest.raises(TaskNotFoundError):
        repository.get(999)


def test_get_all_tasks() -> None:
    repository = TaskRepository()
    first_task = Task(1, "Learn Python")
    second_task = Task(2, "Learn SQL")
    repository.add(first_task)
    repository.add(second_task)

    assert repository.get_all() == [first_task, second_task]


def test_update_existing_task() -> None:
    repository = TaskRepository()
    original = Task(1, "Learn Python", status=TaskStatus.TODO)
    updated = Task(1, "Learn SQL", status=TaskStatus.IN_PROGRESS)

    repository.add(original)
    repository.update(updated)

    assert repository.get(1) == updated
    assert len(repository.get_all()) == 1


def test_update_nonexistent_task() -> None:
    repository = TaskRepository()

    with pytest.raises(TaskNotFoundError):
        repository.update(Task(1, "Learn Python"))

    assert repository.get_all() == []


def test_repository_independence() -> None:
    first_repository = TaskRepository()
    second_repository = TaskRepository()
    task = Task(1, "Learn Python")
    first_repository.add(task)

    assert first_repository.get_all() == [task]
    assert second_repository.get_all() == []


def test_get_all_returns_new_list() -> None:
    repository = TaskRepository()
    original = Task(1, "Learn Python")

    repository.add(original)

    task_list = repository.get_all()
    task_list.clear()

    assert task_list == []
    assert repository.get_all() == [original]
