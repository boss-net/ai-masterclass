import pytest
from modules.task_orchestration.task_management import TaskManager


def test_task_creation():
    manager = TaskManager()
    task = manager.create_task(name="test_task", priority=1, data={"input": "test"})
    assert task is not None
    assert task.priority == 1


def test_task_processing():
    manager = TaskManager()
    task = manager.create_task(name="test_task", priority=1, data={"input": "test"})
    results = manager.process_all()
    assert len(results) == 1


def test_task_priority():
    manager = TaskManager()

    # Create tasks with different priorities
    task1 = manager.create_task(name="low_priority", priority=2, data={})

    task2 = manager.create_task(name="high_priority", priority=1, data={})

    # Process tasks - high priority should be processed first
    results = manager.process_all()
    assert results[0].task.name == "high_priority"
