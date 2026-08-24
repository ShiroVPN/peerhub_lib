__all__ = [
    "define_task",
    "route_task_to_peerhub",
]

from collections.abc import Coroutine
from types import CoroutineType
from typing import Callable, TypeVar
from uuid import UUID

from taskiq import AsyncTaskiqDecoratedTask
from taskiq.kicker import AsyncKicker

T = TypeVar("T")


def define_task(
    task: AsyncTaskiqDecoratedTask[..., CoroutineType[object, object, T]],
):
    def wrapper(func: Callable[..., CoroutineType[object, object, T]]):
        new_task = task.broker.register_task(func, task.task_name)
        return new_task

    return wrapper


C = TypeVar("C", bound=Coroutine[object, object, object])


def route_task_to_peerhub(
    task: AsyncTaskiqDecoratedTask[..., C],
    peerhub_id: UUID,
) -> AsyncKicker[..., C]:
    return task.kicker().with_labels(peerhub_id=str(peerhub_id))
