from typing import Type
import telethon.tl.types
from telethon import TelegramClient
from telethon import events
from scrapper import IMessageChecker


class Transport:
    def __is_forward(self, event) -> bool:
        peer = event.peer_id
        if isinstance(peer, telethon.tl.types.PeerChat):
            if peer.chat_id == self.__group_id:
                return False
        if isinstance(peer, telethon.tl.types.PeerChannel):
            if peer.channel_id == self.__group_id:
                return False
        return True

    def __init__(
            self,
            api_id: str,
            api_hash: str,
            message_checker: Type[IMessageChecker],
            group_id: int
    ):
        self.__client = TelegramClient('session_name', int(api_id), api_hash)
        self.__client.start()
        self.__message_checker = message_checker
        self.__group_id = group_id

        @self.__client.on(events.NewMessage())
        async def handler(event):
            message = event.message.message.lower()
            if self.__is_forward(event):
                if self.__message_checker.check(message):
                    try:
                        await self.__client.forward_messages(self.__group_id, event.message)
                    except Exception as e:
                        print(str(e))

    def start(self):
        self.__client.run_until_disconnected()
