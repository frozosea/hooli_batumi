import os
from dotenv import load_dotenv

from telethon import TelegramClient, events


class ChatBot:
    __client: TelegramClient

    def __init__(self, api_id: str, api_hash: str, phone: str, password: str, send_to_group_id: int):
        self.__client = TelegramClient('session_name', int(api_id), api_hash)
        self.__client.start(phone=lambda: phone, password=lambda: password)

        @self.__client.on(events.NewMessage())
        async def handler(event):
            message = event.message
            for word in ["сниму", "снимем", "снять", "снимаем", "арендовать", "аренда", "арендуем", "арендую",
                         "rent"]:
                if word in message.lower() and event.peer_id.chat_id != send_to_group_id:
                    await self.__client.forward_messages(send_to_group_id, event.message)

    def start(self):
        self.__client.run_until_disconnected()


if __name__ == '__main__':
    try:
        load_dotenv()
    except Exception:
        print("No .env file")
    ChatBot(os.environ.get("API_ID"), os.environ.get("API_HASH"), os.environ.get("PHONE_NUMBER"),
            os.environ.get("PASSWORD"), int(os.environ.get("SEND_GROUP_ID"))).start()
