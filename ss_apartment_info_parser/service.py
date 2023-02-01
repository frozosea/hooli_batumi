from typing import Type
from request import IRequest
from scrapper import IParser
from entity import Apartment
from repository import IProxyRepository


class Service:
    def __init__(self, request: Type[IRequest], parser: Type[IParser], repository: Type[IProxyRepository]):
        self.__request = request
        self.__parser = parser
        self.__repository = repository

    async def get(self, url: str) -> Apartment:
        try:
            string_html = await self.__request.send(url, self.__repository.get())
            return self.__parser.parse(string_html)
        except Exception as e:
            print(e)
            return None
