import logging
import os
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup

from aiohttp import ClientSession

from dotenv import load_dotenv


class HeadersGenerator:

    def generate(self) -> dict:
        return {
            'authority': 'www.myhome.ge',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4',
            'cache-control': 'max-age=0',
            'referer': 'https://www.myhome.ge/ru/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }


class Request:
    headers_generator: HeadersGenerator

    def __init__(self):
        self.headers_generator = HeadersGenerator()

    async def send(self, url: str) -> str:
        async with ClientSession() as session:
            response = await session.get(url, headers=self.headers_generator.generate())

            return str(await response.text())


@dataclass(unsafe_hash=True)
class Result:
    Images: List[str]
    Address: str
    UsdPrice: float
    LariPrice: float
    Floor: str
    Description: str
    Square: int
    Benefits: List[str]


class Parser:
    def get_images(self, soup: BeautifulSoup) -> List[str]:
        try:
            return [item["data-src"] for item in soup.find_all(class_="swiper-lazy h-100")]
        except:
            return []

    def get_address(self, soup: BeautifulSoup) -> str:
        try:
            return re.sub('[\t\n]+', '', soup.find(class_="address").text)
        except:
            return ""

    def get_usd_price(self, soup: BeautifulSoup) -> float:
        try:
            return soup.select_one(
                "#main_block > div.detail-page > aside > div.price-box > div._asd > div > div.d-flex.mb-2.align-items-center.justify-content-between > div.price.d-flex.align-items-center.justify-content-between > span")[
                "data-price-usd"]
        except:
            return -1

    def get_gel_price(self, soup: BeautifulSoup) -> float:
        try:
            return soup.select_one(
                "#main_block > div.detail-page > aside > div.price-box > div._asd > div > div.d-flex.mb-2.align-items-center.justify-content-between > div.price.d-flex.align-items-center.justify-content-between > span")[
                "data-price-gel"]
        except:
            return ""

    def get_square(self, soup: BeautifulSoup) -> float:
        raw = soup.select_one(
            "#main_block > div.detail-page > div.main-features.row.no-gutters > div:nth-child(1) > div > span:nth-child(1)")
        str_square = raw.text.split(" ")[0]
        return float(str_square)

    def get_floor(self, soup: BeautifulSoup) -> str:
        try:
            s = soup.select_one(
                "#main_block > div.detail-page > div.main-features.row.no-gutters > div.col-6.col-lg-4.mb-0.mb-md-4.mb-lg-0.d-flex.align-items-center.mb-4.pr-2.pr-lg-0.tooltip-theme-arrows.tooltip-target.tooltip-element-attached-bottom.tooltip-element-attached-center.tooltip-target-attached-top.tooltip-target-attached-center.tooltip-abutted.tooltip-abutted-top > div > span:nth-child(1)")
            return re.sub('[\t\n]+', '', s.text)
        except:
            return ""

    def get_benefits(self, soup: BeautifulSoup) -> List[str]:
        try:
            return [re.sub('[\t\n]+', '', t.text) for t in
                    soup.select_one("#main_block > div.detail-page > div.amenities > div.row").find_all("span",
                                                                                                        class_="d-block")
                    if len(t["class"]) == 1]
        except:
            return []

    def get_description(self, soup: BeautifulSoup) -> str:
        try:
            return re.sub('[\t\n]+', '', soup.find(class_="pr-comment translated").text)
        except:
            return ""

    def parse(self, string_html: str) -> Result:
        soup = BeautifulSoup(string_html, "lxml")
        return Result(
            Images=self.get_images(soup),
            Address=self.get_address(soup),
            Floor=self.get_floor(soup),
            Description=self.get_description(soup),
            UsdPrice=self.get_usd_price(soup),
            LariPrice=self.get_gel_price(soup),
            Benefits=self.get_benefits(soup),
            Square=self.get_square(soup)
        )


class Service:
    request: Request
    parser: Parser

    def __init__(self):
        self.request = Request()
        self.parser = Parser()

    async def get(self, url: str) -> Result:
        try:
            string_html = await self.request.send(url)
            return self.parser.parse(string_html)
        except Exception as e:
            print(e)
            return None


logging.basicConfig(level=logging.INFO)
API_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
dp = Dispatcher(bot)

service = Service()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply("Привет! отправь ссылку с myhome.ge и получи объявление")


def generate_messsage(r: Result):
    return f"""Описание: {r.Description} \nПлощадь: {r.Square}\nЦена: {r.UsdPrice}$/{r.LariPrice if r.LariPrice else 0}₾\n\nАдрес: {r.Address} {("," + r.Floor) if r.Floor else ""}\n\nДополнительно: {", ".join(r.Benefits)}"""


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def parse(message: types.Message):
    if "https://www.myhome.ge" in message.text:
        await message.reply("В процессе парсинга...")
        result = await service.get(message.text)
        media = types.MediaGroup()
        for index, image in enumerate(result.Images, 0):
            if index < 9:
                media.attach_photo(types.InputFile.from_url(image), generate_messsage(result) if index == 0 else "")
        await bot.send_media_group(chat_id=message.chat.id, media=media)


if __name__ == '__main__':
    try:
        load_dotenv()
    except Exception:
        print("No .env file")
    executor.start_polling(dp)
