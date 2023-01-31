from __future__ import annotations

import datetime
from typing import Type

from task import TaskProvider
from cron import ICronManager
from entity import AddTask
from repository import ICronRepository


class Service:
    def __init__(self, task_provider: TaskProvider, cron: Type[ICronManager], repository: Type[ICronRepository]):
        self.__task_provider = task_provider
        self.__cron = cron
        self.__repository = repository

    def add(self, url: str, group_id: int | float) -> None:
        task = self.__task_provider.get_task(start_date=datetime.datetime.now(), url=url, chat_id=group_id,
                                             max_flat_number=1)
        self.__cron.add(task_id=str(group_id), fn=task, trigger='interval', hours=1)
        self.__repository.add_job(AddTask(Url=url, GroupId=group_id))

    def remove(self, id: int | str) -> None:
        self.__cron.remove(str(id))

    def retry_tasks(self):
        all_jobs = self.__repository.get_jobs()
        if len(all_jobs):
            for job in all_jobs:
                task = self.__task_provider.get_task(max_flat_number=10, url=job.Url, chat_id=job.GroupId)
                self.__cron.add(task_id=str(job.GroupId), fn=task, trigger='interval', hours=1)
