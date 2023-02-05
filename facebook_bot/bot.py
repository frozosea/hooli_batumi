from typing import List
from aiogram import Dispatcher
from aiogram import types
from aiogram.utils import executor

from service import Service


class Bot:
    def __init__(self, service: Service, bot, allowed_users: List[int]):
        self.__bot = bot
        self.__dp = Dispatcher(self.__bot)
        self.__service = service
        self.__allowed_users = allowed_users

        @self.__dp.message_handler(commands=['start'])
        async def cmd_start(message: types.Message):
            await message.reply(
                """Привет! это Hooli real estate fb scrapper schedule бот,
                    
                    Этот бот принадлежит Hooli real estate inc. 
                    Если Вы не являетесь сотрудником нашей компании, пожалуйста, не пользуйтесь этим ботом. Спасибо!
                """)

        @self.__dp.message_handler()
        async def parse(message: types.Message):
            user_id = message.from_user.id
            if user_id not in self.__allowed_users:
                await self.__bot.send_messsage(chat_id=message.chat.id,
                                               text="У вас нет прав для использования этого бота!\nОбратитесь к адмнистратору")

    def run(self):
        executor.start_polling(self.__dp)
