import os
import json
from typing import List
from dotenv import load_dotenv
from aiogram import Bot
from entity import Category
from cron import CronManager
from scrapper import NumberParser
from provider import ClientProvider
from repository import Repository
from provider import PropertySaleObjectProvider
from provider import PropertyRentObjectProvider
from task import TaskProvider
from facebook import FacebookMessageProvider
from service import Service
from bot import Bot


def get_categories() -> List[Category]:
    with open("config.json", "r") as file:
        return [Category(GroupId=d["GroupId"], Eval=d["Eval"]) for d in json.loads(file.read())]


if __name__ == '__main__':
    try:
        load_dotenv()
    except:
        print("no .env file")
    bot = Bot(token=os.environ.get("BOT_TOKEN"))

    cron = CronManager()
    cron.start()
    repository = Repository().migrate()
    client_provider = ClientProvider(repository=repository, chat_id=int(os.environ.get("RENT_REQUEST_GROUP_ID")),
                                     bot=bot)

    sale_object_provider = PropertySaleObjectProvider(repository=repository,
                                                      chat_id=int(os.environ.get("SALE_OBJECTS_GROUP_ID")), bot=bot)

    rent_object_provider = PropertyRentObjectProvider(repository=repository, bot=bot, number_parser=NumberParser(),
                                                      categories=get_categories())

    providers = [client_provider, sale_object_provider, rent_object_provider]

    task_provider = TaskProvider(providers=providers)

    LIMIT_OF_MESSAGES = int(os.environ.get("LIMIT_OF_MESSAGES"))

    fb_providers = [FacebookMessageProvider(cookies="cookies.txt", limit=LIMIT_OF_MESSAGES, group_id=int(group)) for
                    group in os.environ.get("FACEBOOK_GROUP_IDS").split(";")]

    service = Service(cron=cron, task=task_provider)

    MINUTES = int(os.environ.get("MINUTES"))

    for fb in fb_providers:
        service.add(fb, MINUTES)

    Bot(service=service, bot=bot,
        allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
