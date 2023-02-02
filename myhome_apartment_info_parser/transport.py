from typing import List
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from service import Service
from entity import Apartment


class Transport:

    def __init__(self, token, allowed_users: List[int], service: Service):
        self.__bot = Bot(token=token)
        self.__dp = Dispatcher(self.__bot)

        self.__service = service
        self.__allowed_users = allowed_users

        @self.__dp.message_handler(commands='start')
        async def cmd_start(message: types.Message):
            await message.reply("""Привет! этот бот принадлежит Hooli real estate inc. Отправь ссылку и получи выгрузку.
            Если Вы не являетесь сотрудником нашей компании, пожалуйста, не пользуйтесь этим ботом. Спасибо!""")

        @self.__dp.message_handler()
        async def parse(message: types.Message):
            user_id = message.from_user.id
            if user_id in self.__allowed_users:
                if "myhome.ge" in message.text:
                    await message.reply("В процессе парсинга... Это может занять несколько минут...")
                    try:
                        result = await self.__service.get(message.text)
                        print(result)
                        media = types.MediaGroup()
                        for index, image in enumerate(result.Images, 0):
                            if index <= 9:
                                media.attach_photo(types.InputFile.from_url(image),
                                                   self.__generate_messsage(result) if index == 0 else "")
                        await self.__bot.send_media_group(chat_id=message.chat.id, media=media)
                    except:
                        await message.answer("Упс... Что-то пошло не так, попробуйте позже или обратитесь к администратору")
            else:
                await message.answer("У вас нет доступа к данному боту, обратитесь к администратору!")

    @staticmethod
    def __generate_messsage(r: Apartment):
        return f"""Описание: {r.Description} \nПлощадь: {r.Square}\nЦена: {r.UsdPrice}$/{r.LariPrice if r.LariPrice else 0}₾\n\nАдрес: {r.Address} {("," + r.Floor) if r.Floor else ""}\n\nДополнительно: {", ".join(r.Benefits)}"""

    def start(self):
        return executor.start_polling(self.__dp)
