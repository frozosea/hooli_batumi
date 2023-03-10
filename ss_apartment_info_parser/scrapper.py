import re
from typing import List
from abc import ABC
from abc import abstractmethod
from bs4 import BeautifulSoup
from entity import Apartment


class IParser(ABC):
    @abstractmethod
    def parse(self, string_html: str) -> Apartment:
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
            return re.sub('[\t\n]+', '', soup.find(class_="pr-comment translated").text)
        except:
            return ""

    def parse(self, string_html: str) -> Apartment:
        soup = BeautifulSoup(string_html, "lxml")
        return Apartment(
            Images=self.__get_images(soup),
            Address=self.__get_address(soup),
            Floor=self.__get_floor(soup),
            UsdPrice=self.__get_usd_price(soup),
            BedroomQuantity=self.__get_bedroom_quantity(soup),
            RoomQuantity=self.__get_room_quantity(soup),
            Square=self.__get_square(soup)
        )
