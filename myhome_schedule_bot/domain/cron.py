from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Callable
from dataclasses import dataclass

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


@dataclass()
class Time:
    Hours: str | int
    Minutes: str | int
    Seconds: str | int


@dataclass()
class Job:
    Id: any
    Func: Callable
    Time: Time


class ICronManager(ABC):
    @abstractmethod
    def add(self, task_id: any, fn: Callable, **kwargs) -> Job:
        ...

    @abstractmethod
    def remove(self, task_id: any) -> None:
        ...

    @abstractmethod
    def start(self):
        ...


class CronManager(ICronManager):

    def __init__(self):
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        self.__manager = AsyncIOScheduler(jobstores=jobstores)

    def add(self, task_id: any, fn: Callable, *args, **kwargs) -> Job:
        self.__manager.add_job(fn, id=task_id, *args, **kwargs)
        return None

    def remove(self, task_id: any) -> None:
        self.__manager.remove(task_id)

    def start(self):
        self.__manager.start()
