import datetime
import threading
from typing import Type
from typing import Coroutine
from delivery import IDelivery
from repository import IRepository
from provider import FlatProvider

from data_parser import Provider as AppartmentInfoParser


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

    def get_task(self, start_date: datetime.datetime, url: str, **kwargs) -> Coroutine:
        async def task():
            try:
                last_apart = await self.__provider.get_last_appartment(url)
            except Exception as e:
                print(e)
                return
            print(last_apart)
            apart_from_repository = self.__repository.get(last_apart.Id)
            if not apart_from_repository:
                threading.Thread(target=self.__repository.add(last_apart)).start()
                info_about_flat = await self.__appartment_info_parser.get(last_apart.Url)
                print(info_about_flat)
                await self.__delivery.send(result=info_about_flat, **kwargs)

        return task
