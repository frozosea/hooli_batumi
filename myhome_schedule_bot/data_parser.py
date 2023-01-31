import dataclasses
import json
from typing import Type
from aiohttp import ClientSession
import re
from abc import ABC
from abc import abstractmethod
from bs4 import BeautifulSoup
from typing import List
from repository import IProxyRepository


@dataclasses.dataclass()
class Apartment:
    Images: List[str]
    Address: str
    UsdPrice: float
    LariPrice: float
    Floor: str
    Description: str
    Square: int
    Benefits: List[str]
    Url: str
    PhoneNumber: str


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
        return open("script.js", "r").read() % url

    async def send(self, url: str, proxy: str) -> str:
        async with ClientSession() as session:
            response = await session.post(f"{self.__browser_url}/task", headers={"Authorization": self.__auth_password},
                                          data=json.dumps({"script": self.__get_script(url),
                                                           "options": {"upstreamProxyUrl": proxy}}))
            j = await response.json()
        return j["output"]


class IParser(ABC):
    @abstractmethod
    def parse(self, url: str, string_html: str) -> Apartment:
        ...


class Parser(IParser):
    @staticmethod
    def __get_images(soup: BeautifulSoup) -> List[str]:
        try:
            return [item["data-src"] for item in soup.find_all(class_="swiper-lazy h-100")]
        except:
            return []

    @staticmethod
    def __get_address(soup: BeautifulSoup) -> str:
        try:
            return re.sub('[\t\n]+', '', soup.find(class_="address").text)
        except:
            return ""

    @staticmethod
    def __get_usd_price(soup: BeautifulSoup) -> float:
        try:
            return soup.select_one(
                "#main_block > div.detail-page > aside > div.price-box > div._asd > div > div.d-flex.mb-2.align-items-center.justify-content-between > div.price.d-flex.align-items-center.justify-content-between > span")[
                "data-price-usd"]
        except:
            return -1

    @staticmethod
    def __get_gel_price(soup: BeautifulSoup) -> float:
        try:
            return soup.select_one(
                "#main_block > div.detail-page > aside > div.price-box > div._asd > div > div.d-flex.mb-2.align-items-center.justify-content-between > div.price.d-flex.align-items-center.justify-content-between > span")[
                "data-price-gel"]
        except:
            return ""

    @staticmethod
    def __get_square(soup: BeautifulSoup) -> float:
        raw = soup.select_one(
            "#main_block > div.detail-page > div.main-features.row.no-gutters > div:nth-child(1) > div > span:nth-child(1)")
        str_square = raw.text.split(" ")[0]
        return str_square

    @staticmethod
    def __get_floor(soup: BeautifulSoup) -> str:
        try:
            s = soup.select_one(
                "#main_block > div.detail-page > div.main-features.row.no-gutters > div.col-6.col-lg-4.mb-0.mb-md-4.mb-lg-0.d-flex.align-items-center.mb-4.pr-2.pr-lg-0.tooltip-theme-arrows.tooltip-target.tooltip-element-attached-bottom.tooltip-element-attached-center.tooltip-target-attached-top.tooltip-target-attached-center.tooltip-abutted.tooltip-abutted-top > div > span:nth-child(1)")
            return re.sub('[\t\n]+', '', s.text)
        except:
            return ""

    @staticmethod
    def __get_benefits(soup: BeautifulSoup) -> List[str]:
        try:
            return [re.sub('[\t\n]+', '', t.text) for t in
                    soup.select_one("#main_block > div.detail-page > div.amenities > div.row").find_all("span",
                                                                                                        class_="d-block")
                    if len(t["class"]) == 1]
        except:
            return []

    @staticmethod
    def __get_description(soup: BeautifulSoup) -> str:
        try:
            return re.sub('[\t\n]+', '', soup.find(class_="pr-comment translated").text)
        except:
            return ""

    @staticmethod
    def __get_phone_number(soup: BeautifulSoup) -> str:
        try:
            raw_number = soup.select_one(
                '#main_block > div.detail-page > div.statement-author.align-items-center.flex-wrap > button > div > var').text
            number = re.sub(r"\n\t\s", '', raw_number).strip()
            return f"+995 {number}"
        except Exception as e:
            print(e)
            return ""

    def parse(self, url: str, string_html: str) -> Apartment:
        soup = BeautifulSoup(string_html, "lxml")
        return Apartment(
            Images=self.__get_images(soup),
            Address=self.__get_address(soup),
            Floor=self.__get_floor(soup),
            Description=self.__get_description(soup),
            UsdPrice=self.__get_usd_price(soup),
            LariPrice=self.__get_gel_price(soup),
            Benefits=self.__get_benefits(soup),
            Square=self.__get_square(soup),
            Url=url,
            PhoneNumber=self.__get_phone_number(soup)
        )


class Provider:
    def __init__(self, request: Type[IRequest], parser: Type[IParser], proxy_repository: Type[IProxyRepository]):
        self.__req = request
        self.__parser = parser
        self.__proxy_repository = proxy_repository

    async def get(self, url: str) -> Apartment:
        try:
            string_html = await self.__req.send(url, self.__proxy_repository.get())
            return self.__parser.parse(url=url, string_html=string_html)
        except Exception as e:
            print(e)
            return None
