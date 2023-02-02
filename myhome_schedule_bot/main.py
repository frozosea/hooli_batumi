# import asyncio
# import logging
# import os
#
# from dotenv import load_dotenv
# from aiogram import Bot
# from data_parser import Request
# from data_parser import Parser
# from data_parser import Provider as ApartmentDataParser
#
# from cron import CronManager
# from request import Request as DomainRequest
#
# from provider import FlatProvider
# from repository import Repository
# from repository import CronRepository
# from delivery import Delivery
# from task import TaskProvider
# from service import Service
# from bot import Bot as TgBot
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     try:
#         load_dotenv()
#     except Exception:
#         print("No .env file")
#
#     apartment_data_parser = ApartmentDataParser(
#         Request(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")), Parser())
#     cron = CronManager()
#     cron.start()
#     flat_provider = FlatProvider(
#         DomainRequest(browser_url=os.environ.get("BROWSER_URL"), auth_password=os.environ.get("AUTH_PASSWORD")))
#     repository = Repository()
#     repository.migrate()
#     bot = Bot(token=os.environ.get("BOT_TOKEN"))
#     delivery = Delivery(bot)
#     task_provider = TaskProvider(delivery, repository, flat_provider, apartment_data_parser)
#     service = Service(task_provider, cron, CronRepository().migrate())
#     service.retry_tasks()
#     TgBot(service, bot, allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()

import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot
from data_parser import SimpleRequest
from data_parser import BrowserRequest
from data_parser import Parser
from data_parser import Provider as ApartmentDataParser

from cron import CronManager
from request import SimpleRequest as DomainSimpleRequest
from request import BrowserRequest as DomainBrowserRequest

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

    proxies = os.environ.get("PROXIES")
    if not proxies:
        proxies = ""

    proxy_repo = ProxyRepository([proxy for proxy in proxies.split(";")])
    cron = CronManager()
    cron.start()

    USE_BROWSER = int(os.environ.get("USE_BROWSER"))
    if USE_BROWSER == 1:
        apartment_data_parser = ApartmentDataParser(
            BrowserRequest(os.environ.get("BROWSER_URL"), os.environ.get("AUTH_PASSWORD"),os.environ.get("MACHINE_IP")), Parser(),
            proxy_repo)
        flat_provider = FlatProvider(
            DomainBrowserRequest(os.environ.get("BROWSER_URL"), os.environ.get("AUTH_PASSWORD"),os.environ.get("MACHINE_IP")),
            proxy_repo)
    else:
        apartment_data_parser = ApartmentDataParser(
            SimpleRequest(), Parser(),
            proxy_repo)
        flat_provider = FlatProvider(
            DomainSimpleRequest(),
            proxy_repo)

    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    delivery = Delivery(bot)
    task_provider = TaskProvider(delivery, Repository().migrate(), flat_provider, apartment_data_parser)
    if int(os.environ.get("TEST")) == 1:
        asyncio.get_event_loop().run_until_complete(task_provider.task(max_flat_number=4,
                                                                       url="https://www.myhome.ge/ru/s/%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0-%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%B4%D0%BE%D0%BC-%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%BA%D0%BE%D0%BC%D0%B5%D1%80%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D1%8C-%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D1%83%D1%87%D0%B0%D1%81%D1%82%D0%BE%D0%BA-%D0%B7%D0%B5%D0%BC%D0%BB%D0%B8-%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%B3%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B8%D1%86%D0%B0-%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D0%B8?Keyword=%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D0%B8&AdTypeID=1&PrTypeID=1.2.4.5.7&regions=687578743.687611312.687586034.688350922.689701920.689678147.688137211.687602533.688330506.687618311.-1&fullregions=687578743.687611312.687586034.688350922.689701920.689678147.688137211.687602533.688330506.687618311.-1&districts=62176122.319380261.58416723.2953929439.58420997.152297954.61645269.6273968347.58416582.58416672.58377946.152296218.26445359.58873656.28484892.56755168.63067869.2022621279.28044707.28241800.906139527.671983000.176163232.26445392.156581483.62672532.26398517.59459975.58533738.159975019.25758451.1665472307.1299980477.1665566310.1650325628.2185664.25758453.744327681.738255266.78253509.740627378.62283470.4756361456.153933047.5965823289.754181576.61793385.28484811.190594087.1650325626.58518757.63067872.798496409.59618380.754288889.79409026.28484762.61973817.1665595256.385341956.58545182.737627093.737816010.48950942.1651252654.737845964.742404417.45372844.422195753.58777365.2172993612.3132855457.79697734.124158072.457315667.28045012.906117284.5469869.26445372.2035926160.678485529.5995653.199479145.199479146.919489314.411355292.26768649.411355289.6274385718.57792577.155180894.28463059.1989303835.61442032.62236890.31796071.215361176.77767105.153824708.25687735.61447673.222115143.152296216.3656305640.26444838.737255803.737261604.58499142.164033350&cities=1996871&GID=1996871",
                                                                       ))
    else:
        service = Service(task_provider, cron, CronRepository().migrate())
        service.retry_tasks()
        TgBot(service, bot, allowed_users=[int(user) for user in os.environ.get("ALLOWED_USERS").split(";")]).run()
