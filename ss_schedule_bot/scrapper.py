import datetime
import re

import requests
from bs4 import BeautifulSoup

from entity import LastAppartment


class Parser:
    @staticmethod
    def __parse_id(soup: BeautifulSoup, number: int) -> int:
        raw = soup.select_one(f"#list > div:nth-child({number})")
        if raw:
            id = raw.attrs["data-id"]
            if id:
                return int(id)
        return None

    def __parse_href(self, soup: BeautifulSoup, number: int) -> str:
        try:
            tag = soup.select_one(
                f"#list > div:nth-child({number}) > div.latest_article_each_in > div.MobileArticleLayout > div.latest_left.latest_left_mobile > div.latest_desc > a")
            if tag.has_attr("href"):
                return f'https://ss.ge{tag.attrs["href"]}'
        except:
            return ""

    def parse(self, html: str, number: int) -> LastAppartment:
        soup = BeautifulSoup(html, "lxml")
        return LastAppartment(self.__parse_id(soup=soup, number=number), self.__parse_href(soup=soup, number=number))

