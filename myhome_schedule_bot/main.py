import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from myhome_schedule_bot.apartment_data_parser.request import Request
from myhome_schedule_bot.apartment_data_parser.ua_generator import UserAgentGenerator
from myhome_schedule_bot.apartment_data_parser.parser import Parser
from myhome_schedule_bot.apartment_data_parser.provider import Provider as ApartmentDataParser

from myhome_schedule_bot.domain.cron import CronManager
from myhome_schedule_bot.domain.request import Request as DomainRequest

from myhome_schedule_bot.domain.provider import FlatProvider
from myhome_schedule_bot.domain.repository import Repository
from myhome_schedule_bot.domain.delivery import Delivery
from myhome_schedule_bot.domain.task import TaskProvider
from myhome_schedule_bot.domain.service import Service
from myhome_schedule_bot.domain.bot import Bot as TgBot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        load_dotenv()
    except Exception:
        print("No .env file")

    apartment_data_parser = ApartmentDataParser(Request(browser_url="http://api.findmycargo.ru:8010/task/", auth_password="pridumal94"), Parser())
    r = asyncio.run(apartment_data_parser.get(
        "https://www.myhome.ge/ru/pr/11962348/Продается-дом-Дигмисвели-Улица-барон-де-Бай-6-комнат"))
    print(r)
    # cron = CronManager()
    # cron.start()
    # flat_provider = FlatProvider(DomainRequest())
    # repository = Repository()
    # repository.migrate()
    # bot = Bot(token=os.environ.get("BOT_TOKEN"))
    # delivery = Delivery(bot)
    # task_provider = TaskProvider(delivery, repository, flat_provider, apartment_data_parser)
    # service = Service(task_provider, cron)
    # TgBot(service, bot, [int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
