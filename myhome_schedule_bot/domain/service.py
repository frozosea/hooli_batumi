from __future__ import annotations

import datetime
from typing import Type

from task import TaskProvider
from myhome_schedule_bot.domain.cron import ICronManager


class Service:
    def __init__(self, task_provider: TaskProvider, cron: Type[ICronManager], ):
        self.__task_provider = task_provider
        self.__cron = cron

    def add(self, url: str, group_id: int | float) -> None:
        task = self.__task_provider.get_task(start_date=datetime.datetime.now(), url=url, chat_id=group_id)
        self.__cron.add(task_id=group_id, fn=task, trigger='interval', minutes=1)

    def remove(self, id: int | str) -> None:
        self.__cron.remove(id)
