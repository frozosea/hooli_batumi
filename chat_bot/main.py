import os

import telethon.tl.types
from dotenv import load_dotenv

from telethon import TelegramClient, events


class ChatBot:
    __client: TelegramClient
    __send_to_group_id: int

    def __is_forward(self, event) -> bool:
        peer = event.peer_id
        if isinstance(peer, telethon.tl.types.PeerChat):
            if peer.chat_id == self.__send_to_group_id:
                return False
        return True

    def __init__(self, api_id: str, api_hash: str, send_to_group_id: int):
        self.__client = TelegramClient('session_name', int(api_id), api_hash)
        self.__client.start()
        self.__send_to_group_id = send_to_group_id

        @self.__client.on(events.NewMessage())
        async def handler(event):
            message = event.message.message.lower()
            for word in ["сниму", "снимем", "снять", "снимаем", "арендовать", "аренда", "арендуем", "арендую",
                         "rent"]:
                if word in message.lower() and self.__is_forward(event):
                    await self.__client.forward_messages(send_to_group_id, event.message)

    def start(self):
        self.__client.run_until_disconnected()


if __name__ == '__main__':
    try:
        load_dotenv()
    except Exception:
        print("No .env file")
    ChatBot(os.environ.get("API_ID"), os.environ.get("API_HASH"), int(os.environ.get("SEND_GROUP_ID"))).start()
