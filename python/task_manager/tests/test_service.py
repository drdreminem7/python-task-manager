from typing import Any

import pytest

from task_manager.exceptions import (
    DuplicateTaskError,
    InvalidTaskError,
    TaskNotFoundError,
)
from task_manager.models import Task, TaskStatus
from task_manager.repository import TaskRepository
from task_manager.service import TaskService


@pytest.fixture
def repo() -> TaskRepository:
    return TaskRepository()


@pytest.fixture
def service(repo: TaskRepository) -> TaskService:
    return TaskService(repo)


def test_create_task(repo: TaskRepository, service: TaskService) -> None:
    created_task = service.create_task(1, "Learn Python")
    expected_task = Task(1, "Learn Python")

    assert created_task == expected_task
    assert repo.get(1) == expected_task


@pytest.mark.parametrize("invalid_id", [-1, 0, True, "1", 1.5, None])
def test_create_task_with_invalid_id(
    invalid_id: Any, repo: TaskRepository, service: TaskService
) -> None:
    with pytest.raises(InvalidTaskError):
        service.create_task(invalid_id, "Learn Python")

    assert repo.get_all() == []


def test_create_task_with_duplicate_id(
    repo: TaskRepository, service: TaskService
) -> None:
    original_task = service.create_task(1, "Learn Python")

    with pytest.raises(DuplicateTaskError):
        service.create_task(1, "Learn SQL")

    assert repo.get(1) == original_task
    assert repo.get_all() == [original_task]


@pytest.mark.parametrize("invalid_title", ["", "   ", None, 123, True])
def test_create_task_with_invalid_title(
    invalid_title: Any, repo: TaskRepository, service: TaskService
) -> None:
    with pytest.raises(InvalidTaskError):
        service.create_task(1, invalid_title)

    assert repo.get_all() == []


def test_create_task_with_normalized_title(
    repo: TaskRepository, service: TaskService
) -> None:
    created_task = service.create_task(1, "   Learn Python     ")

    assert created_task.title == "Learn Python"
    assert repo.get(1).title == "Learn Python"


def test_get_existing_task(repo: TaskRepository, service: TaskService) -> None:
    task = service.create_task(1, "Learn Python")

    existing_task = service.get_task(1)

    assert task == existing_task


def test_get_nonexistent_task(repo: TaskRepository, service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.get_task(999)


def test_list_tasks(repo: TaskRepository, service: TaskService) -> None:
    first = service.create_task(1, "Learn Python")
    second = service.create_task(2, "Learn SQL")
    third = service.create_task(3, "Learn GO")

    assert service.list_tasks() == [first, second, third]
    assert len(service.list_tasks()) == 3


def test_list_tasks_empty(repo: TaskRepository, service: TaskService) -> None:
    assert service.list_tasks() == []


def test_update_task(repo: TaskRepository, service: TaskService) -> None:
    original_task = service.create_task(1, "Learn Python")
    updated_task = service.update_task(1, "Learn GO")

    assert updated_task.title == "Learn GO"
    assert repo.get(1) == updated_task
    assert original_task.title == "Learn Python"
    assert updated_task is not original_task


def test_update_preserves_status(repo: TaskRepository, service: TaskService) -> None:
    original_task = Task(1, "Learn Python", TaskStatus.IN_PROGRESS)
    repo.add(original_task)

    updated_task = service.update_task(1, "Learn GO")

    assert updated_task.status == TaskStatus.IN_PROGRESS
    assert repo.get(1).status == TaskStatus.IN_PROGRESS
    assert updated_task.title == "Learn GO"


def test_update_nonexistent_task(repo: TaskRepository, service: TaskService) -> None:
    with pytest.raises(TaskNotFoundError):
        service.update_task(1, "Learn GO")


def test_update_invalid_title(repo: TaskRepository, service: TaskService) -> None:
    original_task = service.create_task(1, "Learn Python")

    with pytest.raises(InvalidTaskError):
        service.update_task(1, "  ")

    assert repo.get(1) == original_task
    assert repo.get_all() == [original_task]
