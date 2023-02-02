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


class BrowserRequest(IRequest):

    def __init__(self, browser_url: str, auth_password: str, machine_ip: str = None):
        self.__browser_url = browser_url
        self.__auth_password = auth_password
        self.__machine_ip = machine_ip

    @staticmethod
    def __get_script(url: str) -> str:
        data = open("script.js", "r").read()
        return data.replace("await agent.goto('%s');", f"await agent.goto('{url}');")

    async def send(self, url: str, proxy: str) -> str:
        p = {
            "options": {
                "timezoneId": "Asia/Tbilisi",
                "viewport": {
                    "width": 1920,
                    "height": 1080,
                    "deviceScaleFactor": 1
                },
                "geolocation": {
                    "latitude": 41.6941,
                    "longitude": 44.8337,
                    "accuracy": 45
                },
                "blockedResourceTypes": ["BlockCssAssets", "BlockImages", "BlockFonts", "BlockIcons", "BlockMedia"],
                "locale": "ru-GE"
            },
            "script": self.__get_script(url)
        }
        if proxy:
            p["options"]["upstreamProxyUrl"] = proxy
            if self.__machine_ip:
                p["options"]["upstreamProxyIpMask"] = {
                    "ipLookupService": "api.ipify.org",
                    "proxyIp": re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", proxy)[0],
                    "publicIp": self.__machine_ip
                }
        payload = json.dumps(p)
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


class SimpleRequest(IRequest):
    async def send(self, url: str, proxy: str) -> str:
        headers = {
            'authority': 'ss.ge',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4',
            # 'cookie': 'modal_shown_landing_realestate=0; screenResolution2=true; wallindex=6; __zlcmid=1E3lXokgBejqm2h; _hjSessionUser_550566=eyJpZCI6IjBlZTE3MTBjLTRlZTItNTk3MC05MDU4LWRiNzJlMmY3ZTc5MCIsImNyZWF0ZWQiOjE2NzQzNjc5MDM2NzQsImV4aXN0aW5nIjp0cnVlfQ==; RealEstateType=Flat; viewed-application-ids=%5B6167275%2C6120686%2C3232163%2C5710876%2C6168693%2C5253181%2C5746789%2C6178540%2C6172355%2C6159087%2C6049980%2C6214507%2C6195952%2C6189460%2C6214425%2C5304996%2C4964932%2C4238485%2C6183717%2C5903560%2C4429856%2C6215258%2C6162647%2C6181154%2C3745633%2C2960253%2C6204266%2C6195915%2C6211692%2C5798420%2C6182952%2C6117100%2C6140818%2C3225758%2C6224548%2C6232208%5D; _gid=GA1.2.747596871.1675244663; RealEstateDealType=For%20Rent; ListingLink=https%3A%2F%2Fss.ge%2Fru%2F%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C%2Fl%2F%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0%2F%D0%90%D1%80%D0%B5%D0%BD%D0%B4%D0%B0; .AspNetCore.Antiforgery.ZQZ9-5TPDZ8=CfDJ8BVgksY10KhBgxIHE4YE-KR7MTQqa7nhyubvKHPR6NsSGrjuJ8qM1NzoDNNCbzW_zuOe576rijSah1ObuUrVVrnFp6QUkHqmSZwG2Y98ux8Y-OWomtKWI9dwTs6gGP-LK-erYmyjQItnxlxMalsZvss; _hjIncludedInSessionSample=0; _hjSession_550566=eyJpZCI6ImJlZmEyZjA4LWZiNTMtNGMwYy05OTJiLWI2MGYyOTAyMjcxNiIsImNyZWF0ZWQiOjE2NzUzMTc1MDAwNzYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga=GA1.1.83976452.1674367903; _ga_6TNNPZXX61=GS1.1.1675317502.24.1.1675317511.51.0.0',
            'referer': 'https://ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        if proxy:
            if "http" in proxy:
                response = requests.get(url, headers=headers, proxies={"http": proxy})
            elif "https" in proxy:
                response = requests.get(url, headers=headers, proxies={"https": proxy})
            else:
                raise Exception("wrong proxy url")
        else:
            response = requests.get(url, headers=headers)
        print(response.status_code)
        return response.text


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
                "#main-body > div.all_page_blocks > div.container.realestateDtlSlider > div.col-md-9.col-xs-9.DetailedMd9 > div:nth-child(1) > div.DetailedPageAllBodyBLock > div > div.article_item_desc > div.translate_block > div > span.details_text").text)[
                   :3500]
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

    async def get(self, url: str, proxy: str = None) -> Apartment:
        try:
            string_html = await self.request.send(url, proxy if proxy else self.__proxy_repository.get())
            result = self.parser.parse(string_html=string_html, url=url)
            return result
        except Exception as e:
            print(f"ERROR IN APARTMENT DATA PARSER SERVICE: {e}")
            return None
