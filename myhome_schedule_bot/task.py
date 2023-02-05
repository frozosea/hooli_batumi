import time
from typing import Type
from typing import Coroutine
from delivery import IDelivery
from repository import IRepository
from provider import FlatProvider


class TaskProvider:
    def __init__(
            self,
            delivery: Type[IDelivery],
            repository: Type[IRepository],
            flat_provider: FlatProvider,
    ):
        self.__delivery = delivery
        self.__repository = repository
        self.__provider = flat_provider

    async def task(self, max_flat_number: int, url: str, **kwargs):
        uri = url
        if "ajax" not in url.lower():
            uri = url + "&Ajax=1"
        try:
            last_aparts = await self.__provider.get_last_appartments(url=uri, max_flat_number=max_flat_number,
                                                                     proxy="")
        except Exception as e:
            print(e)
            return
        print(last_aparts)
        for apart in last_aparts:
            apart_exists = self.__repository.check_exists(apart.Id)
            print(f"{apart.Id} ALREADY IN REPOSITORY" if apart_exists else f"{apart.Id} NOT IN REPOSITORY")
            if not apart_exists:
                try:
                    self.__repository.add(apart)
                    print(apart)
                except Exception as e:
                    print(e)
                    continue

    def get_task(self, max_flat_number: int, url: str, proxy: str = None, **kwargs) -> Coroutine:
        async def task():
            uri = url
            if "ajax" not in url.lower():
                uri = url + "&Ajax=1"
            try:
                last_aparts = await self.__provider.get_last_appartments(url=uri, max_flat_number=max_flat_number,
                                                                         proxy=proxy)
            except Exception as e:
                print(e)
                return
            print(last_aparts)
            for apart in last_aparts:
                apart_from_repository = self.__repository.check_exists(apart.Id)
                print(f"{apart.Id} ALREADY IN REPOSITORY" if apart_from_repository else f"{apart.Id} NOT IN REPOSITORY")
                if not apart_from_repository:
                    try:
                        self.__repository.add(apart)
                        await self.__delivery.send(result=apart, **kwargs)
                        time.sleep(40)
                    except Exception as e:
                        time.sleep(40)
                        print(e)
                        continue

        return task
