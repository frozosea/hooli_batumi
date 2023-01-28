import datetime
import threading
from typing import Type
from typing import Coroutine
from delivery import IDelivery
from repository import IRepository
from provider import FlatProvider

from apartment_data_parser.provider import Provider as AppartmentInfoParser


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
            last_appart = await self.__provider.get_last_appartment(url)
            appart_from_repository = self.__repository.get(last_appart.Id)
            if not appart_from_repository and last_appart.AddDate > start_date:
                threading.Thread(target=self.__repository.add(last_appart)).start()
                info_about_flat = await self.__appartment_info_parser.get(last_appart.Url)
                await self.__delivery.send(result=info_about_flat, **kwargs)

        return task
