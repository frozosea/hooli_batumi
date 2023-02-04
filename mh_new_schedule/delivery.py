from abc import ABC
from abc import abstractmethod

import aiogram
from aiogram import types

from entity import Apartment


class IDelivery(ABC):
    @abstractmethod
    async def send(self, result: Apartment, **kwargs) -> None:
        ...


class Delivery(IDelivery):

    def __init__(self, bot: aiogram.Bot):
        self.__bot = bot

    @staticmethod
    def __generate_messsage(r: Apartment):
        return f"""Описание: {r.Description} \nПлощадь: {r.Square}\nЦена: {r.UsdPrice}$\n\nАдрес: {r.Address} {("," + str(r.Floor)) if r.Floor else ""}\n \n\n Url: {r.Url}"""[
               :3800]

    async def send(self, result: Apartment, **kwargs) -> None:
        media = types.MediaGroup()
        for index, image in enumerate(result.Images, 0):
            if index <= 9:
                media.attach_photo(types.InputFile.from_url(image),
                                   self.__generate_messsage(result) if index == 0 else "")
        await self.__bot.send_media_group(chat_id=kwargs.get("chat_id"), media=media)
