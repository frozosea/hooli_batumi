import re
from abc import ABC
from abc import abstractmethod
from typing import List
from bs4 import BeautifulSoup
from entity import Apartment


class IParser(ABC):
    @abstractmethod
    def parse(self, string_html: str) -> Apartment:
        ...


class Parser(IParser):
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
        return str_square

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

    def parse(self, string_html: str) -> Apartment:
        soup = BeautifulSoup(string_html, "lxml")
        return Apartment(
            Images=self.get_images(soup),
            Address=self.get_address(soup),
            Floor=self.get_floor(soup),
            Description=self.get_description(soup),
            UsdPrice=self.get_usd_price(soup),
            LariPrice=self.get_gel_price(soup),
            Benefits=self.get_benefits(soup),
            Square=self.get_square(soup)
        )
