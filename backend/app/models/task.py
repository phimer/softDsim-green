import logging
import time
from typing import Set

from deprecated.classic import deprecated
from django.db import models
from django.db.models import QuerySet

import pickle
import numpy as np
import base64

from app.models.user_scenario import UserScenario

# from app.src.util.task_util import get_numpy_tasks_as_task_list


class NumpyTasks(models.Model):
    """This saves Tasks to the database as an encoded numpy matrix of all the tasks of one user scenario"""

    tasks = models.BinaryField()
    user_scenario = models.ForeignKey(
        UserScenario, on_delete=models.CASCADE, related_name="numpy_tasks"
    )

    @staticmethod
    def get_as_numpy_task_set(user_scenario=None, user_scenario_id=None):

        if user_scenario:
            # user_scenario = UserScenario.objects.filter(id=user_scenario_id)
            base_64_tasks = NumpyTasks.objects.filter(user_scenario=user_scenario)[
                0
            ].tasks
        else:
            base_64_tasks = NumpyTasks.objects.filter(
                user_scenario_id=user_scenario_id
            )[0].tasks

        np_bytes = base64.b64decode(base_64_tasks)

        np_array = pickle.loads(np_bytes)

        task_list = []
        for i in range(len(np_array)):
            task_list.append(NumpyTask().build_from_array(np_array[i]))
        return set(task_list)

    @staticmethod
    def get_as_cached_tasks(user_scenario_id):
        """returns numpy tasks as a cached scenario object"""
        return CachedTasks(user_scenario_id=user_scenario_id)

    @staticmethod
    def save_tasks(task_list, user_scenario):
        """saves list of task as an encoded numpy array to the database"""

        np_base64 = task_list_to_base64_string(task_list)
        # save to db
        NumpyTasks.objects.update(tasks=np_base64, user_scenario=user_scenario)

    @staticmethod
    def create_numpy_tasks_in_db(
        easy_tasks, medium_tasks, hard_tasks, user_scenario: UserScenario
    ):
        """Create tasks as numpy_tasks in database"""

        task_list = []

        for i in range(easy_tasks):
            task_list.append(NumpyTask(difficulty=1))
        for i in range(medium_tasks):
            task_list.append(NumpyTask(difficulty=2))
        for i in range(hard_tasks):
            task_list.append(NumpyTask(difficulty=3))

        tasks_base64 = task_list_to_base64_string(task_list)
        NumpyTasks.objects.create(tasks=tasks_base64, user_scenario=user_scenario)


class NumpyTask:
    def __init__(
        self,
        difficulty=1,
        done=False,
        bug=False,
        correct_specification=True,
        integration_tested=False,
        unit_tested=False,
    ):
        self.difficulty = difficulty
        self.done = done
        self.bug = bug
        self.correct_specification = correct_specification
        self.integration_tested = integration_tested
        self.unit_tested = unit_tested

    def as_array(self):
        return [
            self.difficulty,
            1 if self.done else 0,
            1 if self.bug else 0,
            1 if self.correct_specification else 0,
            1 if self.integration_tested else 0,
            1 if self.unit_tested else 0,
        ]

    def build_from_array(self, arr):
        """builds task from numpy array"""
        self.difficulty = arr[0]
        self.done = True if arr[1] == 1 else False
        self.bug = True if arr[2] == 1 else False
        self.correct_specification = True if arr[3] == 1 else False
        self.integration_tested = True if arr[4] == 1 else False
        self.unit_tested = True if arr[5] == 1 else False

        return self


def task_list_to_base64_string(task_list: [NumpyTask]):
    """turns list of numpy tasks into base64 string"""

    # turn all tasks to arrays
    numpy_task_list = [t.as_array() for t in task_list]
    # turn list into numpy array
    numpy_matrix = np.array(numpy_task_list)
    # turn numpy array into bytes
    np_bytes = pickle.dumps(numpy_matrix)
    # turn bytes into base64
    np_base64 = base64.b64encode(np_bytes)

    return np_base64


@deprecated(reason="This function is now build into NumpyTasks object")
def get_numpy_tasks_as_task_set(user_scenario=None, user_scenario_id=None):
    """gets tasks in list from encoded numpy array in database"""

    if user_scenario:
        # user_scenario = UserScenario.objects.filter(id=user_scenario_id)
        base_64_tasks = NumpyTasks.objects.filter(user_scenario=user_scenario)[0].tasks
    else:
        base_64_tasks = NumpyTasks.objects.filter(user_scenario_id=user_scenario_id)[
            0
        ].tasks

    np_bytes = base64.b64decode(base_64_tasks)

    np_array = pickle.loads(np_bytes)

    task_list = []
    for i in range(len(np_array)):
        task_list.append(NumpyTask().build_from_array(np_array[i]))
    return set(task_list)


class Task(models.Model):
    # id = models.AutoField(primary_key=True, db_index=True)
    difficulty = models.PositiveIntegerField()
    done = models.BooleanField(default=False)
    bug = models.BooleanField(default=False)
    correct_specification = models.BooleanField(default=True)
    unit_tested = models.BooleanField(default=False)
    integration_tested = models.BooleanField(default=False)
    predecessor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    user_scenario = models.ForeignKey(
        UserScenario, on_delete=models.CASCADE, related_name="tasks"
    )

    # Methods to get tasks by their state


class TaskStatus:
    def __init__(self, user_scenario_id):
        self.tasks = NumpyTasks.get_as_cached_tasks(user_scenario_id=user_scenario_id)
        # self.tasks = CachedTasks(user_scenario_id=user_scenario_id)

    def todo(self, scenario_id) -> QuerySet:
        """Returns all tasks that are not yet done."""
        return self.tasks.todo()
        return Task.objects.filter(user_scenario_id=scenario_id, done=False)

    def done(self, scenario_id) -> QuerySet:
        """Returns all tasks that are done, but not yet tested. Includes tasks with and
        without bug"""
        return Task.objects.filter(
            user_scenario_id=scenario_id,
            done=True,
            unit_tested=False,
            integration_tested=False,
        )

    def unit_tested(self, scenario_id) -> QuerySet:
        """Returns all tasks that are successfully unit tested (no bug found)"""
        return Task.objects.filter(
            user_scenario_id=scenario_id,
            done=True,
            bug=False,
            unit_tested=True,
            integration_tested=False,
        )

    def integration_tested(self, scenario_id) -> QuerySet:
        """Returns all tasks that are successfully integration tested."""
        return Task.objects.filter(
            user_scenario_id=scenario_id,
            integration_tested=True,
        )

    def bug(self, scenario_id) -> QuerySet:
        """Returns all tasks that are done, but a bug was found by a unit test."""
        return Task.objects.filter(
            user_scenario_id=scenario_id, done=True, unit_tested=True, bug=True
        )

    def bug_undiscovered(self, scenario_id) -> QuerySet:
        """Returns all tasks that have a bug that is unknown to the team/user"""
        return Task.objects.filter(
            user_scenario_id=scenario_id, done=True, unit_tested=False, bug=True
        )

    def done_wrong_specification(self, scenario_id) -> QuerySet:
        """Returns all tasks that were done with a wrong specification unknown to the team/user"""
        return Task.objects.filter(
            user_scenario_id=scenario_id, done=True, correct_specification=False
        )

    def solved(self, scenario_id) -> QuerySet:
        """Returns all tasks that are done for the current UserScenario."""
        return Task.objects.filter(done=True, user_scenario_id=scenario_id)

    def accepted(self, scenario_id) -> QuerySet:
        """Returns all tasks that are accepted by customer."""
        return Task.objects.filter(
            user_scenario_id=scenario_id,
            done=True,
            bug=False,
            correct_specification=True,
        )

    def rejected(self, scenario_id) -> QuerySet:
        """Returns all tasks that are rejected by customer."""
        all = Task.objects.filter(user_scenario_id=scenario_id)
        acc = TaskStatus.accepted(scenario_id)
        rej = all.exclude(id__in=acc)
        return rej


class CachedTasks:
    """This is a version of the TasksStatus class that is somehow cached. You
    can use it by instantiating one object by passing the scenario_id. Then use
    it to get and update tasks as long as you want and in the end call the save
    method to save the changes to the database.
    """

    def __init__(self, user_scenario_id):
        start = time.perf_counter()
        # changed this to NumpyTasks
        # self.tasks: Set[Task] = set(Task.objects.filter(user_scenario_id=scenario_id))
        self.tasks: Set[NumpyTask] = NumpyTasks.get_as_numpy_task_set(
            user_scenario_id=user_scenario_id
        )
        logging.info(f"Getting Tasks took {time.perf_counter() - start} seconds")
        # todo raise if no scenario exists

    def todo(self) -> QuerySet:
        """Returns all tasks that are not yet done."""
        return set(filter(lambda t: not t.done, self.tasks))

    def done(self) -> Set[NumpyTask]:
        """Returns all tasks that are done, but not yet tested. Includes tasks with and
        without bug"""
        return set(
            filter(
                lambda t: t.done and not t.unit_tested and not t.integration_tested,
                self.tasks,
            )
        )

    def unit_tested(self) -> Set[NumpyTask]:
        """Returns all tasks that are successfully unit tested (no bug found)"""
        return set(
            filter(
                lambda t: t.done
                and not t.bug
                and t.unit_tested
                and not t.integration_tested,
                self.tasks,
            )
        )

    def integration_tested(self) -> Set[NumpyTask]:
        """Returns all tasks that are successfully integration tested."""
        return set(filter(lambda t: t.integration_tested, self.tasks))

    def bug(self) -> Set[NumpyTask]:
        """Returns all tasks that are done, but a bug was found by a unit test."""
        return set(filter(lambda t: t.done and t.bug and t.unit_tested, self.tasks))

    def bug_undiscovered(self) -> Set[NumpyTask]:
        """Returns all tasks that have a bug that is unknown to the team/user"""
        return set(filter(lambda t: t.done and t.bug and not t.unit_tested, self.tasks))

    def done_wrong_specification(self) -> Set[NumpyTask]:
        """Returns all tasks that were done with a wrong specification unknown to the team/user"""
        return set(filter(lambda t: t.done and not t.correct_specification, self.tasks))

    def solved(self) -> Set[NumpyTask]:
        """Returns all tasks that are done for the current UserScenario."""
        return set(filter(lambda t: t.done, self.tasks))

    def accepted(self) -> Set[NumpyTask]:
        """Returns all tasks that are accepted by customer."""
        return set(
            filter(
                lambda t: t.done and not t.bug and t.correct_specification, self.tasks
            )
        )

    def rejected(self) -> Set[NumpyTask]:
        """Returns all tasks that are rejected by customer."""
        return {t for t in self.tasks if t not in self.accepted()}

    def save(self, scenario):
        """Bulk updates all tasks to database."""
        start = time.perf_counter()
        # Task.objects.bulk_update(
        #     self.tasks,
        #     [
        #         "done",
        #         "bug",
        #         "unit_tested",
        #         "integration_tested",
        #         "correct_specification",
        #     ],
        # )

        # save numpyTasks
        print("saving numpy tasks in task.py CachedTasks.save()")
        NumpyTasks.save_tasks(task_list=self.tasks, user_scenario=scenario)
        logging.warning(f"Saving tasks took {time.perf_counter() - start} seconds")
