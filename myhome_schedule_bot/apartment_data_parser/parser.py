import re
from typing import List
from abc import ABC
from abc import abstractmethod
from bs4 import BeautifulSoup

from entity import Appartment


class IParser(ABC):
    @abstractmethod
    def parse(self, url: str, string_html: str) -> Appartment:
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

    def parse(self, url: str, string_html: str) -> Appartment:
        soup = BeautifulSoup(string_html, "lxml")
        return Appartment(
            Images=self.__get_images(soup),
            Address=self.__get_address(soup),
            Floor=self.__get_floor(soup),
            Description=self.__get_description(soup),
            UsdPrice=self.__get_usd_price(soup),
            LariPrice=self.__get_gel_price(soup),
            Benefits=self.__get_benefits(soup),
            Square=self.__get_square(soup),
            Url=url
        )
