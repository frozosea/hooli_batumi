from abc import ABC
from abc import abstractmethod
import aiogram
from aiogram import types
from entity import Message


class IDelivery(ABC):
    @abstractmethod
    async def send(self, **kwargs):
        ...


class ClientMessageDelivery(IDelivery):
    def __init__(self, bot: aiogram.Bot, chat_id: int):
        self.__chat_id = chat_id
        self.__bot = bot

    @staticmethod
    def _generate_message(message: Message) -> str:
        return f"Текст: {message.message}\nСсылка на пост: {message.url}\nСсылка на пользователя：{message.user_url}\nДата поста: {message.date.date()}"

    async def send(self, message: Message):
        try:
            await self.__bot.send_message(chat_id=self.__chat_id, text=self._generate_message(message))
        except Exception as e:
            print(f"SEND CLIENT MESSAGE ERROR: {e}")


class SaleObjectDelivery(ClientMessageDelivery):
    async def send(self, message: Message):
        try:
            if len(message.images) > 0:
                media = types.MediaGroup()
                for index, image in enumerate(message.images, 0):
                    if index <= 9:
                        media.attach_photo(types.InputFile.from_url(image),
                                           self._generate_message(message) if index == 0 else "")
                await self.__bot.send_media_group(chat_id=self.__chat_id, media=media)
            else:
                await self.__bot.send_message(chat_id=self.__chat_id, text=self._generate_message(message))
        except Exception as e:
            print(f"SEND PROPERTY SALE OBJECT MESSAGE ERROR: {e}")


class RentObjectDelivery(SaleObjectDelivery):
    async def send(self, message: Message, chat_id: int):
        try:
            if len(message.images) > 0:
                media = types.MediaGroup()
                for index, image in enumerate(message.images, 0):
                    if index <= 9:
                        media.attach_photo(types.InputFile.from_url(image),
                                           self._generate_message(message) if index == 0 else "")
                await self.__bot.send_media_group(chat_id=chat_id, media=media)
            else:
                await self.__bot.send_message(chat_id=chat_id, text=self._generate_message(message))
        except Exception as e:
            print(f"SEND PROPERTY SALE OBJECT MESSAGE ERROR: {e}")
