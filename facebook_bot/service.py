import random
from typing import Type
from cron import ICronManager
from task import TaskProvider
from facebook import IFacebookMessageProvider
from request import IRequest as CookieProvider


class Service:
    def __init__(self, cron: Type[ICronManager], task: TaskProvider, cookie_provider: Type[CookieProvider]):
        self.__cron = cron
        self.__task = task
        self.__cookie_provider = cookie_provider

    def add(self, fb: Type[IFacebookMessageProvider], minutes: int):
        try:
            self.__cron.add(
                task_id=str(random.Random().randint(1, 1000)),
                fn=self.__task.get_task(fb),
                trigger='interval',
                minutes=minutes
            )
        except Exception as e:
            print(f"CANNOT ADD TASK WITH EXCEPTION: {e}")

    def add_cookies_writer_task(self, minutes: int):
        try:
            self.__cron.add(
                task_id=str(random.Random().randint(1, 1000)),
                fn=self.__task.get_write_cookies_task(self.__cookie_provider),
                trigger='interval',
                minutes=minutes
            )
        except Exception as e:
            print(f"CANNOT ADD TASK WITH EXCEPTION: {e}")
