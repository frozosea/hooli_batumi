import time
from typing import Type
from typing import Coroutine
from delivery import IDelivery
from repository import IRepository
from provider import FlatProvider
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
            print(e)
            return
        print(last_aparts)
        time.sleep(100)
        for apart in last_aparts:
            apart_from_repository = self.__repository.get(apart.Id)
            if not apart_from_repository:
                self.__repository.add(apart)
            info_about_flat = await self.__appartment_info_parser.get(apart.Url)
            print(info_about_flat)
            time.sleep(100)

    def get_task(self, max_flat_number: int, url: str, proxy: str = None, **kwargs) -> Coroutine:
        async def task():
            try:
                last_aparts = await self.__provider.get_last_appartments(url=url, max_flat_number=max_flat_number,
                                                                         proxy=proxy)
            except Exception as e:
                print(e)
                return
            time.sleep(100)
            for apart in last_aparts:
                apart_from_repository = self.__repository.get(apart.Id)
                print(f"{apart.Id} ALREADY IN REPOSITORY" if apart_from_repository else f"{apart.Id} NOT IN REPOSITORY")
                if not apart_from_repository:
                    try:
                        self.__repository.add(apart)
                        info_about_flat = await self.__appartment_info_parser.get(apart.Url, proxy=proxy)
                        await self.__delivery.send(result=info_about_flat, **kwargs)
                        time.sleep(100)
                    except Exception as e:
                        print(e)
                        time.sleep(90)
                        continue

        return task
