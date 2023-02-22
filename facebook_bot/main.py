import asyncio
import os
import json
from typing import List
from dotenv import load_dotenv
from aiogram import Bot
from entity import Category
from cron import CronManager
from scrapper import NumberParser
from provider import ClientOnRentProvider
from repository import Repository
from provider import PropertySaleObjectProvider
from provider import PropertyRentObjectProvider
from task import TaskProvider
from facebook import FacebookMessageProvider
from service import Service
from bot import Bot as Transport
from repository import Repository
from request import Request


def get_categories() -> List[Category]:
    with open("config.json", "r") as file:
        return [Category(GroupId=d["GroupId"], Eval=d["Eval"]) for d in json.loads(file.read())]


if __name__ == '__main__':
    try:
        load_dotenv()
    except:
        print("no .env file")
    bot = Bot(token=os.environ.get("BOT_TOKEN"))

    c = CronManager()
    c.start()
    repository = Repository().migrate()
    client_provider = ClientOnRentProvider(repository=repository, chat_id=int(os.environ.get("RENT_REQUEST_GROUP_ID")),
                                           bot=bot)

    sale_object_provider = PropertySaleObjectProvider(repository=repository,
                                                      chat_id=int(os.environ.get("SALE_OBJECTS_GROUP_ID")), bot=bot)

    rent_object_provider = PropertyRentObjectProvider(repository=repository, bot=bot, number_parser=NumberParser(),
                                                      categories=get_categories())

    providers = [client_provider, sale_object_provider, rent_object_provider]
    cookie_provider = Request(os.environ.get("FACEBOOK_LOGIN"), os.environ.get("FACEBOOK_PASSWORD"), "cookies.json")
    task_provider = TaskProvider(providers=providers, cookie_path="cookies.json")

    LIMIT_OF_MESSAGES = int(os.environ.get("LIMIT_OF_MESSAGES"))

    fb_providers = [FacebookMessageProvider(limit=LIMIT_OF_MESSAGES, group_id=group) for
                    group in os.environ.get("FACEBOOK_GROUP_IDS").split(";")]
    print(len(fb_providers))
    service = Service(cron=c, task=task_provider,cookie_provider=cookie_provider)

    MINUTES = int(os.environ.get("MINUTES"))

    service.add_cookies_writer_task(MINUTES - 3)

    for fb in fb_providers:
        service.add(fb, MINUTES)
    Transport(service=service, bot=bot,
              allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
