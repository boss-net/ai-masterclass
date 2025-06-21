import pytest
from modules.task_orchestration.task_management import TaskManager, WorkflowTask


def test_workflow_creation():
    manager = TaskManager()

    # Create workflow with multiple steps
    workflow = WorkflowTask(
        name="test_workflow",
        steps=[
            {"name": "step1", "type": "basic"},
            {"name": "step2", "type": "conditional"},
            {"name": "step3", "type": "parallel"},
        ],
    )

    assert workflow is not None
    assert len(workflow.steps) == 3


def test_workflow_execution():
    manager = TaskManager()

    # Create and add workflow
    workflow = WorkflowTask(
        name="test_workflow",
        steps=[
            {"name": "step1", "type": "basic"},
            {"name": "step2", "type": "conditional"},
        ],
    )
    manager.add_task(workflow)

    # Process workflow
    results = manager.process_all()

    # Verify results
    assert len(results) == 1
    assert results[0].task.name == "test_workflow"
    assert results[0].status == "completed"


def test_workflow_error_handling():
    manager = TaskManager()

    # Create workflow with failing step
    workflow = WorkflowTask(
        name="test_workflow",
        steps=[
            {"name": "step1", "type": "basic"},
            {"name": "step2", "type": "failing"},
        ],
    )
    manager.add_task(workflow)

    # Process workflow
    results = manager.process_all()

    # Verify error handling
    assert results[0].status == "failed"
    assert results[0].error is not None
