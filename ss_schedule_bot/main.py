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
    flat_provider = FlatProvider(
        DomainRequest(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")))
    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    delivery = Delivery(bot)
    task_provider = TaskProvider(delivery, Repository().migrate(), flat_provider, apartment_data_parser)
    # service = Service(task_provider, cron, CronRepository().mingrate())
    # # service.retry_tasks()
    # service.add(
    #     url="https://ss.ge/ru/недвижимость/l/Квартира/Продается?MunicipalityId=95&CityIdList=95&subdistr=44%2C45%2C46%2C47%2C48%2C49%2C50%2C27%2C26%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C13%2C24%2C14%2C15%2C16%2C17%2C18%2C19%2C32%2C33%2C34%2C35%2C36%2C37%2C53%2C38%2C39%2C40%2C41%2C42%2C43%2C1%2C28%2C29%2C30%2C31%2C20%2C21%2C22%2C23%2C51%2C52&PriceType=false&CurrencyId=1",
    #     group_id=123)
    asyncio.get_event_loop().run_until_complete(task_provider.task(max_flat_number=4,
                                   url="https://ss.ge/ru/недвижимость/l/Квартира/Продается?MunicipalityId=95&CityIdList=95&subdistr=44%2C45%2C46%2C47%2C48%2C49%2C50%2C27%2C26%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C13%2C24%2C14%2C15%2C16%2C17%2C18%2C19%2C32%2C33%2C34%2C35%2C36%2C37%2C53%2C38%2C39%2C40%2C41%2C42%2C43%2C1%2C28%2C29%2C30%2C31%2C20%2C21%2C22%2C23%2C51%2C52&PriceType=false&CurrencyId=1",
                                   ))
    # asyncio.get_event_loop().run_forever()
    # TgBot(service, bot, allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
