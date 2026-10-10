# Task Manager

A small, in-memory task management library built with Python. The project focuses on clean Python engineering practices: typed models, separation of concerns, input validation, explicit exceptions, immutable updates, and automated tests.

## Features

- Create tasks with a unique, positive integer ID and a nonempty title.
- Retrieve an individual task or list all tasks.
- Update a task's title without mutating the original task object.
- Remove leading and trailing whitespace from titles during creation and updates.
- Track a task's status using `TODO`, `IN_PROGRESS`, and `DONE` values.
- Raise specific exceptions for invalid input, duplicate IDs, and missing tasks.

**Scope:** Storage is in memory only. Data is lost when the repository instance is discarded or the process exits. This library does not include a database, REST API, CLI, task deletion, or a public service method for changing task status.

## Project structure

```text
task-manager/
├── task_manager/
│   ├── __init__.py
│   ├── models.py         # Task and TaskStatus
│   ├── repository.py     # In-memory storage
│   ├── service.py        # Validation and application operations
│   └── exceptions.py     # Domain-specific errors
├── tests/
│   ├── test_repository.py
│   └── test_service.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Design

- **`Task`** is a frozen dataclass containing an ID, title, and status. Its default status is `TODO`.
- **`TaskStatus`** is an enum defining the valid task statuses.
- **`TaskRepository`** stores `Task` objects in a dictionary indexed by task ID. It provides `add`, `get`, `get_all`, and `update` methods.
- **`TaskService`** receives a repository through its constructor. It provides `create_task`, `get_task`, `list_tasks`, and `update_task`, applying input validation before delegating storage operations.
- **Updates** create a replacement dataclass instance with `dataclasses.replace`, preserving fields not being changed.

### Exceptions

| Exception            | Raised when                                       |
| -------------------- | ------------------------------------------------- |
| `InvalidTaskError`   | A task ID or title is invalid                     |
| `DuplicateTaskError` | Adding a task whose ID already exists             |
| `TaskNotFoundError`  | Retrieving or updating a task that does not exist |

`InvalidTaskError` and `DuplicateTaskError` inherit from `ValueError`; `TaskNotFoundError` inherits from `KeyError`.

## Getting started

Prerequisites: Python compatible with the version specified in `pyproject.toml`, and [uv](https://docs.astral.sh/uv/).

From the project root, install the project's dependencies:

```bash
uv sync
```

### Example usage

```python
from task_manager.repository import TaskRepository
from task_manager.service import TaskService

repository = TaskRepository()
service = TaskService(repository)

created = service.create_task(1, "  Learn Python  ")
print(created)  # Task title is normalized to "Learn Python"

updated = service.update_task(1, "Master Python")
print(updated)

print(service.get_task(1))
print(service.list_tasks())
```

Task IDs must be positive integers (not booleans). Titles must be strings containing at least one non-whitespace character.

## Testing and quality checks

Run all tests:

```bash
uv run pytest -q
```

Measure test coverage:

```bash
uv run pytest --cov=task_manager --cov-report=term-missing
```

Check lint rules:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Check type annotations:

```bash
uv run mypy task_manager tests
```

Tests cover successful operations, validation failures, duplicate and missing task IDs, title normalization, immutable updates, status preservation, and repository isolation. The test suite uses pytest fixtures and parameterized test cases.

## Purpose

This is an educational project for practicing maintainable Python, not a full-featured task management application. The primary goal is to understand and test each component rather than add a user interface or infrastructure prematurely.
