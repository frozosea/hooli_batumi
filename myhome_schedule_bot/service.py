from __future__ import annotations

import datetime
from typing import Type

from task import TaskProvider
from cron import ICronManager


class Service:
    def __init__(self, task_provider: TaskProvider, cron: Type[ICronManager]):
        self.__task_provider = task_provider
        self.__cron = cron

    def add(self, url: str, group_id: int | float) -> None:
        task = self.__task_provider.get_task(start_date=datetime.datetime.now(), url=url, chat_id=group_id,
                                             max_flat_number=10)
        self.__cron.add(task_id=str(group_id), fn=task, trigger='interval', minutes=5)

    def remove(self, id: int | str) -> None:
        self.__cron.remove(str(id))
