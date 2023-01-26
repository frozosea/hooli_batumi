import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from myhome_schedule_bot.apartment_data_parser.request import Request
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

    apartment_data_parser = ApartmentDataParser(Request(), Parser())
    cron = CronManager()
    cron.start()
    flat_provider = FlatProvider(DomainRequest())
    repository = Repository()
    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    delivery = Delivery(bot)
    task_provider = TaskProvider(delivery, repository, flat_provider, apartment_data_parser)
    service = Service(task_provider, cron)
    TgBot(service, bot, [int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
