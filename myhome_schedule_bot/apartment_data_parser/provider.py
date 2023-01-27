from typing import Type
from myhome_schedule_bot.apartment_data_parser.entity import Appartment
from myhome_schedule_bot.apartment_data_parser.request import IRequest
from myhome_schedule_bot.apartment_data_parser.parser import IParser


class Provider:
    def __init__(self, request: Type[IRequest], parser: Type[IParser]):
        self.__req = request
        self.__parser = parser

    async def get(self, url: str) -> Appartment:
        try:
            string_html = await self.__req.send(url)
            return self.__parser.parse(url=url, string_html=string_html)
        except Exception as e:
            print(e)
            return None
