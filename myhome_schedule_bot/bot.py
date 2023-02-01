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
                """Привет! это Hooli real estate mh schedule бот, отправь сообщение в формате(просто на каждой строке нужное поле, только в таком порядке!): 
                    Command: add/remove 
                    GroupId: айди беседы, куда присылать сообщения с квартирами
                    Url: ссылка (должная уже содержать в себе все фильтры)
                    Proxy: прокси
                    
                    Если команда на удаление, то поле Url,Proxy не нужно, достаточно двух первых.
                    
                    Этот бот принадлежит Hooli real estate inc. 
                    Если Вы не являетесь сотрудником нашей компании, пожалуйста, не пользуйтесь этим ботом. Спасибо!
                """)

        @self.__dp.message_handler()
        async def parse(message: types.Message):
            user_id = message.from_user.id
            if user_id in self.__allowed_users:
                text = message.text
                split = text.split("\n")
                j = {}
                if len(split) == 4:

                    try:
                        j["command"] = split[0].split(":")[1].strip()
                    except:
                        await message.answer("Введите команду в правильном формате!")
                        return

                    try:
                        j["group_id"] = int(split[1].split(":")[1].strip())
                    except:
                        await message.answer("Введите команду в правильном формате!")
                        return

                    command = j["command"]
                    if command == "add":
                        if "https://www.myhome.ge" in message.text:
                            try:
                                j["url"] = split[2].split(":", 1)[1].strip()
                            except:
                                await message.answer("Введите команду в правильном формате!")
                                return
                            try:
                                j["proxy"] = split[3].split(":", 1)[1].strip()
                            except:
                                ...
                            try:
                                self.__service.add(group_id=j["group_id"], url=j["url"],proxy=j["proxy"])
                                await message.answer("Задача была добавлена в бота!")
                            except Exception as e:
                                print(e)
                                await message.answer("Что-то пошло не так, задача не была добавлена...")
                                return
                        else:
                            await message.answer("Введите команду в правильном формате!")
                            return
                    elif command == "remove":
                        try:
                            self.__service.remove(j["group_id"])
                            await message.answer("Задача была удалена из бота!")
                        except Exception as e:
                            print(e)
                            await message.answer("Что-то пошло не так, задача не была удалена...")
                            return

                    else:
                        await message.answer("Введите команду в правильном формате!")
                        return


            else:
                await message.answer("У вас нет доступа к данному боту, обратитесь к администратору!")

    def run(self):
        executor.start_polling(self.__dp)
