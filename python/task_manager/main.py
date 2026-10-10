from task_manager.repository import TaskRepository
from task_manager.service import TaskService


def main():
    repository = TaskRepository()
    service = TaskService(repository)
    service.create_task(1, "Learn Python")
    service.create_task(2, "Study SQL")
    service.create_task(3, " ")


if __name__ == "__main__":
    main()
