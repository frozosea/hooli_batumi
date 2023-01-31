from typing import Type
from typing import List

from request import IRequest

from scrapper import Parser

from entity import LastAppartment

from repository import IProxyRepository


class FlatProvider:
    def __init__(self, request: Type[IRequest], proxy_repository: Type[IProxyRepository]):
        self.__req = request
        self.__parser = Parser()
        self.__proxy_repository = proxy_repository

    async def get_last_appartments(self, max_flat_number: int, url: str) -> List[LastAppartment]:
        html = await self.__req.send(url, proxy=self.__proxy_repository.get())
        l = []
        for i in range(1, max_flat_number):
            try:
                result = self.__parser.parse(html, i)
                l.append(result)
            except Exception as e:
                print(e)
                continue
        return l
