"""Custom exceptions for the task manager."""


class TaskNotFoundError(KeyError):
    """Raised when a requested task does not exist in the repository."""


class DuplicateTaskError(ValueError):
    """Raised when adding a task whose ID already exists."""


class InvalidTaskError(ValueError):
    """Raised when a task ID or title is invalid."""
