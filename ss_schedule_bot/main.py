import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from apartment_data_parser import Request
from apartment_data_parser import Parser
from apartment_data_parser import Service as ApartmentDataParser

from cron import CronManager
from request import Request as DomainRequest

from provider import FlatProvider
from repository import Repository
from repository import CronRepository
from repository import ProxyRepository
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
    proxy_repo = ProxyRepository([proxy for proxy in os.environ.get("PROXIES").split(";")])
    apartment_data_parser = ApartmentDataParser(
        Request(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")), Parser(),
        proxy_repo)
    cron = CronManager()
    cron.start()
    flat_provider = FlatProvider(
        DomainRequest(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")),
        proxy_repo)
    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    delivery = Delivery(bot)
    task_provider = TaskProvider(delivery, Repository().migrate(), flat_provider, apartment_data_parser)
    if bool(os.environ.get("TEST")):
        asyncio.get_event_loop().run_until_complete(task_provider.task(max_flat_number=4,
                                                                       url="https://ss.ge/ru/недвижимость/l/Квартира/Продается/?MunicipalityId=&CityIdList=95",
                                                                       ))
    else:
        service = Service(task_provider, cron, CronRepository().migrate())
        service.retry_tasks()
        TgBot(service, bot, allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
