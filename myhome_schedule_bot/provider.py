from typing import Type
from typing import List

from request import IRequest

from scrapper import IParser

from entity import Apartment

from repository import IProxyRepository


class FlatProvider:
    def __init__(self, request: Type[IRequest], parser: Type[IParser], proxy_repository: Type[IProxyRepository]):
        self.__req = request
        self.__parser = parser
        self.__proxy_repository = proxy_repository

    async def get_last_appartments(self, max_flat_number: int, url: str, proxy: str = None) -> List[Apartment]:
        json = await self.__req.send(url, proxy=proxy if proxy else self.__proxy_repository.get())
        l = []
        for i in range(1, max_flat_number):
            try:
                result = self.__parser.parse(json.data.prs[i])
                l.append(result)
            except Exception as e:
                print(e)
                continue
        return l
