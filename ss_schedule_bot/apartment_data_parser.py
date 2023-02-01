import re
import requests
import json
from dataclasses import dataclass
from typing import List
from typing import Type
from abc import ABC
from abc import abstractmethod
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from repository import IProxyRepository


@dataclass()
class Apartment:
    Images: List[str]
    Address: str
    Description: str
    BedroomQuantity: int
    RoomQuantity: int
    UsdPrice: float
    Floor: str
    Square: int
    PhoneNumber: str
    Url: str


class IRequest(ABC):
    @abstractmethod
    async def send(self, url: str, proxy: str) -> str:
        ...


class Request(IRequest):

    def __init__(self, browser_url: str, auth_password: str):
        self.__browser_url = browser_url
        self.__auth_password = auth_password

    @staticmethod
    def __get_script(url: str) -> str:
        data = open("script.js", "r").read()
        return data.replace("await agent.goto('%s');", f"await agent.goto('{url}');")

    async def send(self, url: str, proxy: str) -> str:
        payload = json.dumps({
            "options": {
                "upstreamProxyUrl": proxy
            },
            "script": self.__get_script(url)
        })
        headers = {
            'Authorization': self.__auth_password,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, proxies={"socks": proxy})
            if response.status_code > 220:
                raise
            return response.text
        except Exception as e:
            print(e)
            async with ClientSession() as session:
                response = await session.post(f"{self.__browser_url}/task", headers=headers, data=payload, )
                j = await response.json()
                task_status = j["status"]
                if task_status == "FAILED" or task_status == "INIT_ERROR" or task_status == "TIMEOUT" or "BAD_ARGS":
                    raise
                return j["output"]


class IParser(ABC):
    @abstractmethod
    def parse(self, string_html: str, url: str) -> Apartment:
        ...


class Parser(IParser):
    @staticmethod
    def __get_images(soup: BeautifulSoup) -> List[str]:
        # DONE
        try:
            tags = soup.find_all(class_="OrdinaryContainer")
            if tags:
                return [item.findChildren('img')[0].attrs["src"] for item in tags]
            else:
                return [item.findChildren('img')[0].attrs["src"] for item in
                        soup.find_all("div", class_="veri-slider-img-sm")]
        except:
            return []

    @staticmethod
    def __get_address(soup: BeautifulSoup) -> str:
        # DONE
        try:
            return re.sub("[\t\n\s]+", '', soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.cadastrcode-streets > div > a").text).strip()
        except:
            return ""

    @staticmethod
    def __get_room_quantity(soup: BeautifulSoup) -> int:
        # DONE
        try:
            return int(soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_parameters > div > div > div.ParamsDetTop > div:nth-child(2) > div.ParamsHdBlk > text").text)
        except:
            return 0

    @staticmethod
    def __get_bedroom_quantity(soup: BeautifulSoup) -> int:
        # DONE
        try:
            return int(soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_parameters > div > div > div.ParamsDetTop > div:nth-child(3) > div.ParamsHdBlk > text").text)
        except:
            return 0

    @staticmethod
    def __get_balcon_quantity(soup: BeautifulSoup) -> int:
        # DONE
        try:
            return int(soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_parameters > div > div > div.ParamsbotProj > div:nth-child(1) > span.PRojeachBlack").text)
        except:
            return 0

    @staticmethod
    def __get_usd_price(soup: BeautifulSoup) -> float:
        # DONE
        try:
            raw = soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.MobilePriceBlockdet > div > div.article_right_price.price").text
            without_space = "".join(raw.split(" "))
            return float(without_space)
        except:
            return -1

    @staticmethod
    def __get_square(soup: BeautifulSoup) -> float:
        # DONE
        try:
            raw = soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_parameters > div > div > div.ParamsDetTop > div.EAchParamsBlocks.WholeFartBlock > div.ParamsHdBlk > text").text
            return float(raw.split("m")[0])
        except:
            return None

    @staticmethod
    def __get_floor(soup: BeautifulSoup) -> str:
        try:
            return "".join(soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_parameters > div > div > div.ParamsDetTop > div:nth-child(4) > div.ParamsHdBlk > text").text.strip().split(
                "\n"))
        except:
            return ""

    @staticmethod
    def __get_description(soup: BeautifulSoup) -> str:
        try:
            return re.sub('[\t\n\r-]+', '', soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_desc > div.translate_block > div > span.details_text").text)[:3500]
        except:
            return ""

    @staticmethod
    def __get_phone_number(soup: BeautifulSoup) -> str:
        try:
            tag = soup.select_one(
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.phone-row--realEstate > div.phone-row-bottom > div > div.phone-row-bottom-item-list.phone-row-bottom-item-list--second > a")
            if tag:
                if tag.has_attr("href"):
                    href = tag.attrs["href"]
                    return f"+995 {href.split('/')[-1]}"
            else:
                number = soup.select_one(
                    "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedRightAll > div > div > div > div.article_author_block.user_article > div > div > div.phone-flex-row.phone-row--realEstate > div.phone-row-top > div.author_contact_info2 > div.UserMObileNumbersBlock > a > span")
                if number:
                    return f"+995 {number.text}"
            raise
        except:
            return ""

    def parse(self, string_html: str, url: str) -> Apartment:
        soup = BeautifulSoup(string_html, "lxml")
        return Apartment(
            Images=self.__get_images(soup),
            Address=self.__get_address(soup),
            Floor=self.__get_floor(soup),
            UsdPrice=self.__get_usd_price(soup),
            BedroomQuantity=self.__get_bedroom_quantity(soup),
            RoomQuantity=self.__get_room_quantity(soup),
            Square=self.__get_square(soup),
            PhoneNumber=self.__get_phone_number(soup),
            Description=self.__get_description(soup),
            Url=url
        )


class Service:
    def __init__(self, request: Type[IRequest], parser: Type[IParser], proxy_repository: Type[IProxyRepository]):
        self.request = request
        self.parser = parser
        self.__proxy_repository = proxy_repository

    async def get(self, url: str) -> Apartment:
        try:
            string_html = await self.request.send(url, self.__proxy_repository.get())
            result = self.parser.parse(string_html=string_html, url=url)
            return result
        except Exception as e:
            print(f"ERROR IN APARTMENT DATA PARSER SERVICE: {e}")
            return None
