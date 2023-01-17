from typing import Dict
from app.cache.scenario import CachedScenario
from app.models.task import Task, TaskStatus, NumpyTasks
from app.dto.response import TasksStatusDTO


def get_tasks_status(session: CachedScenario) -> TasksStatusDTO:
    """Returns a TaskStatusDTO for a current scenario with all data allowed to be seen
    by team/user."""
    return TasksStatusDTO(
        tasks_todo=len(session.tasks.todo()),
        tasks_done=len(session.tasks.done()),
        tasks_unit_tested=len(session.tasks.unit_tested()),
        tasks_integration_tested=len(session.tasks.integration_tested()),
        tasks_bug=len(session.tasks.bug()),
    )


def get_tasks_status_detailed(scenario_id: int) -> Dict[str, int]:
    """Returns json representation of a scenarios tasks status, including data that is
    not allowed to be viewed by team/user."""

    # use numpy tasks instead of old "normal" tasks
    numpy_task_status = NumpyTasks.get_as_cached_tasks(user_scenario_id=scenario_id)
    return {
        "tasks_todo": len(numpy_task_status.todo()),
        "tasks_done": len(numpy_task_status.done()),
        "tasks_unit_tested": len(numpy_task_status.unit_tested()),
        "tasks_integration_tested": len(numpy_task_status.integration_tested()),
        "tasks_bug_discovered": len(numpy_task_status.bug()),
        "tasks_bug_undiscovered": len(numpy_task_status.bug_undiscovered()),
        "tasks_done_wrong_specification": len(
            numpy_task_status.done_wrong_specification()
        ),
    }


def get_tasks_customer_view(scenario_id: int) -> Dict[str, int]:
    """Returns json representation of a scenarios tasks status, as seen from customer"""
    numpy_task_status = NumpyTasks.get_as_cached_tasks(user_scenario_id=scenario_id)
    return {
        "tasks_accepted": len(numpy_task_status.accepted()),
        "tasks_rejected": len(numpy_task_status.rejected()),
    }
