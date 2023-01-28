import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from apartment_data_parser.request import Request
from apartment_data_parser.scrapper import Parser
from apartment_data_parser.provider import Provider as ApartmentDataParser

from domain.cron import CronManager
from domain.request import Request as DomainRequest

from domain.provider import FlatProvider
from domain.repository import Repository
from domain.delivery import Delivery
from domain.task import TaskProvider
from domain.service import Service
from domain.bot import Bot as TgBot

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
    # bot = Bot(token=os.environ.get("BOT_TOKEN"))
    # delivery = Delivery(bot)
    # task_provider = TaskProvider(delivery, repository, flat_provider, apartment_data_parser)
    # service = Service(task_provider, cron)
    # TgBot(service, bot, [int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
