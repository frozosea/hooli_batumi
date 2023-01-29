from typing import Type
from typing import List

from request import IRequest

from scrapper import Parser

from entity import LastAppartment


class FlatProvider:
    def __init__(self, request: Type[IRequest]):
        self.__req = request
        self.__parser = Parser()

    async def get_last_appartments(self, max_flat_number: int, url: str) -> List[LastAppartment]:
        async def __inner(number: int):
            html = await self.__req.send(url)
            print(self.__parser.parse(html=html, number=number))
            return self.__parser.parse(html=html, number=number)
        l = []
        for i in range(5, max_flat_number + 5):
            try:
                result = await __inner(i)
                l.append(result)
            except Exception as e:
                print(e)
                continue
        return l
