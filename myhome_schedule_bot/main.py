import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from apartment_data_parser.request import Request
from apartment_data_parser.scrapper import Parser
from apartment_data_parser.provider import Provider as ApartmentDataParser

from cron import CronManager
from request import Request as DomainRequest

from provider import FlatProvider
from repository import Repository
from delivery import Delivery
from task import TaskProvider
from service import Service
from bot import Bot as TgBot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        load_dotenv()
    except Exception:
        print("No .env file")

    apartment_data_parser = ApartmentDataParser(
        Request(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")), Parser())
    cron = CronManager()
    cron.start()
    flat_provider = FlatProvider(DomainRequest())
    repository = Repository()
    repository.migrate()
    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    delivery = Delivery(bot)
    task_provider = TaskProvider(delivery, repository, flat_provider, apartment_data_parser)
    service = Service(task_provider, cron)
    TgBot(service, bot, [int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
