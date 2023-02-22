from typing import List
from typing import Type
import telethon.tl.types
from telethon import TelegramClient
from telethon import events
from entity import Category
from scrapper import IMessageParser
from scrapper import IMessageChecker
from repository import IRepository


class Transport:
    def __is_forward(self, event) -> bool:
        peer = event.peer_id
        if isinstance(peer, telethon.tl.types.PeerChat):
            return self.__compare_chat_id(self.__categories, peer.chat_id)
        if isinstance(peer, telethon.tl.types.PeerChannel):
            return self.__compare_chat_id(self.__categories, peer.channel_id)
        return False

    def __compare_chat_id(self, categories: List[Category], chat_id) -> bool:
        for c in categories:
            if int(c.GroupId) == int(chat_id):
                return False
        return chat_id not in self.__stopped_list_id

    def __init__(
            self,
            api_id: str,
            api_hash: str,
            message_checker: Type[IMessageChecker],
            message_parser: Type[IMessageParser],
            categories: List[Category],
            stopped_list_id: List[int],
            repository: Type[IRepository]
    ):
        self.__client = TelegramClient('session_name', int(api_id), api_hash)
        self.__client.start()
        self.__message_checker = message_checker
        self.__message_parser = message_parser
        self.__categories = categories
        self.__stopped_list_id = stopped_list_id
        self.__repository = repository

        @self.__client.on(events.NewMessage())
        async def handler(event):
            message = event.message.message.lower()
            if self.__is_forward(event):
                if self.__message_checker.check(message):
                    if not self.__repository.exists(message):
                        try:
                            category = self.__message_parser.get_category(self.__categories, message)
                            await self.__client.forward_messages(category.GroupId, event.message)
                            self.__repository.add(message)
                        except Exception as e:
                            print(str(e))

    def start(self):
        self.__client.run_until_disconnected()
