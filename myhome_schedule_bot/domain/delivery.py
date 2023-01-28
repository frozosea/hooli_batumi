from abc import ABC
from abc import abstractmethod

import aiogram
from aiogram import types

from ..apartment_data_parser.entity import Appartment


class IDelivery(ABC):
    @abstractmethod
    async def send(self, result: Appartment, **kwargs) -> None:
        ...


class Delivery(IDelivery):

    def __init__(self, bot: aiogram.Bot):
        self.__bot = bot

    @staticmethod
    def __generate_messsage(r: Appartment):
        return f"""Описание: {r.Description} \nПлощадь: {r.Square}\nЦена: {r.UsdPrice}$/{r.LariPrice if r.LariPrice else 0}₾\n\nАдрес: {r.Address} {("," + r.Floor) if r.Floor else ""}\n\nДополнительно: {", ".join(r.Benefits)} \n\n Url: {r.Url}"""

    async def send(self, result: Appartment, **kwargs) -> None:
        media = types.MediaGroup()
        for index, image in enumerate(result.Images, 0):
            if index <= 10:
                media.attach_photo(types.InputFile.from_url(image),
                                   self.__generate_messsage(result) if index == 0 else "")
        await self.__bot.send_media_group(chat_id=kwargs.get("chat_id"), media=media)
