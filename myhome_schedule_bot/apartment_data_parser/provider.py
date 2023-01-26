from typing import Type
from entity import Appartment
from request import IRequest
from .parser import IParser


class Provider:
    def __init__(self, request: Type[IRequest], parser: Type[IParser]):
        self.__req = request()
        self.__parser = parser()

    async def get(self, url: str) -> Appartment:
        try:
            string_html = await self.__req.send(url)
            return self.__parser.parse(url=url, string_html=string_html)
        except Exception as e:
            print(e)
            return None
