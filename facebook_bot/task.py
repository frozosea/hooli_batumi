from typing import List
from typing import Type
from typing import Coroutine
from provider import IProvider
from facebook import IFacebookMessageProvider


class TaskProvider:
    def __init__(self, providers: List[Type[IProvider]]):
        self.__providers = providers

    async def __inner_section(self, message):
        for provider in self.__providers:
            await provider.provide(message)

    def get_task(self, fb: Type[IFacebookMessageProvider]) -> Coroutine:
        async def task():
            messages = fb.get()
            for message in messages:
                await self.__inner_section(message)

        return task
