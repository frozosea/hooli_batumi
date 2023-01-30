import asyncio
import threading
from typing import Type
from typing import List
from typing import Coroutine
from delivery import IDelivery
from repository import IRepository
from provider import FlatProvider
from entity import AddTask
from apartment_data_parser import Service as AppartmentInfoParser


class TaskProvider:
    def __init__(
            self,
            delivery: Type[IDelivery],
            repository: Type[IRepository],
            flat_provider: FlatProvider,
            appartment_info_parser: Type[AppartmentInfoParser],
    ):
        self.__delivery = delivery
        self.__repository = repository
        self.__provider = flat_provider
        self.__appartment_info_parser = appartment_info_parser

    async def task(self, max_flat_number: int, url: str, **kwargs):
        try:
            last_aparts = await self.__provider.get_last_appartments(url=url, max_flat_number=max_flat_number)
        except Exception as e:
            return
        print(last_aparts)

        for apart in last_aparts:
            apart_from_repository = self.__repository.get(apart.Id)
            if not apart_from_repository:
                self.__repository.add(apart)
            info_about_flat = await self.__appartment_info_parser.get(apart.Url)
            print(info_about_flat)

    def get_task(self, max_flat_number: int, url: str, **kwargs) -> Coroutine:
        async def task():
            try:
                last_aparts = await self.__provider.get_last_appartments(url=url, max_flat_number=max_flat_number)
            except Exception as e:
                return
            print(last_aparts)

            async def __inner(apart):
                apart_from_repository = self.__repository.get(apart.Id)
                if not apart_from_repository:
                    threading.Thread(target=self.__repository.add(apart)).start()
                info_about_flat = await self.__appartment_info_parser.get(apart.Url)
                print(info_about_flat)
                # await self.__delivery.send(result=info_about_flat, **kwargs)

            asyncio.gather(*[__inner(last_apart) for last_apart in last_aparts])

        return task

    def get_all_jobs(self) -> List[AddTask]:
        return self.__repository.get_jobs()
