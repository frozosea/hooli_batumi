from typing import List
from typing import Type
from typing import Coroutine
from provider import IProvider
from facebook import IFacebookMessageProvider
from repository import IRepository
from request import IRequest


class TaskProvider:
    def __init__(self, providers: List[Type[IProvider]], cookie_path):
        self.__providers = providers
        self.__cookie_path = cookie_path

    async def __inner_section(self, message):
        for provider in self.__providers:
            await provider.provide(message)

    def get_task(self, fb: Type[IFacebookMessageProvider]) -> Coroutine:
        async def task():
            messages = fb.get(self.__cookie_path)
            for message in messages:
                await self.__inner_section(message)

        return task

    @staticmethod
    def get_write_cookies_task(request: Type[IRequest]):
        async def task():
            await request.get_cookies_filepath()

        return task
