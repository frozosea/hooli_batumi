from typing import Type
from request import IRequest
from scrapper import IParser
from entity import Apartment


class Service:
    def __init__(self, request: Type[IRequest], parser: Type[IParser]):
        self.request = request
        self.parser = parser

    async def get(self, url: str) -> Apartment:
        try:
            string_html = await self.request.send(url)
            return self.parser.parse(string_html)
        except Exception as e:
            print(e)
            return None
