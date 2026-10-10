from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.TODO
