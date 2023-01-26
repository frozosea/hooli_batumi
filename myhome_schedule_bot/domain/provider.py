from typing import Type

from request import IRequest

from parser import Parser

from entity import LastAppartment


class FlatProvider:
    def __init__(self, request: Type[IRequest]):
        self.__req = request
        self.__parser = Parser()

    async def get_last_appartment(self, url: str) -> LastAppartment:
        html = await self.__req.send(url)
        return self.__parser.parse(html)
