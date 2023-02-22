import os
from typing import Type
import telethon.tl.types
from dotenv import load_dotenv

from telethon import TelegramClient, events

from repository import IRepository
from repository import Repository
from cron import CronManager


class ChatBot:
    __client: TelegramClient
    __send_to_group_id: int

    def __is_forward(self, event) -> bool:
        print(event.peer_id)
        peer = event.peer_id
        if isinstance(peer, telethon.tl.types.PeerChat):
            if peer.chat_id == self.__send_to_group_id:
                return False
        elif isinstance(peer, telethon.tl.types.PeerChannel):
            if peer.channel_id == self.__send_to_group_id:
                return False
        return True

    def __init__(self, api_id: str, api_hash: str, send_to_group_id: int, repository: Type[IRepository]):
        self.__client = TelegramClient('session_name', int(api_id), api_hash)
        self.__client.start()
        self.__send_to_group_id = send_to_group_id
        self.__repository = repository

        @self.__client.on(events.NewMessage())
        async def handler(event):
            message = event.message.message.lower()
            if self.__is_forward(event):
                try:
                    for word in ["куплю", "купим", "купить", "покупаем", "buy", "bought", "kuplu", "kuplv", "kupim",
                                 "cupim", "cuplu", "kupit"]:
                        if word in message.lower():
                            print(self.__send_to_group_id)
                            print(event.message)
                            print(self.__repository.exists(message))
                            if not self.__repository.exists(message):
                                self.__repository.add(message)
                                await self.__client.forward_messages(self.__send_to_group_id, [event.message])
                except Exception as e:
                    print(e)

    def start(self):
        self.__client.run_until_disconnected()


if __name__ == '__main__':
    try:
        load_dotenv()
    except Exception:
        print("No .env file")

    repository = Repository().migrate()
    cron = CronManager()
    cron.start()
    cron.add("delete_data_from_db", fn=repository.delete_all, trigger="interval", weeks=1)
    ChatBot(os.environ.get("API_ID"), os.environ.get("API_HASH"), int(os.environ.get("SEND_GROUP_ID")),
            repository).start()
