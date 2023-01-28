import datetime
import re

from bs4 import BeautifulSoup

from entity import LastAppartment


class Parser:
    @staticmethod
    def __parse_id(soup: BeautifulSoup) -> int:
        raw = soup.select_one(
            "#main_block > div.d-flex.justify-content-between.p-relative.search-content.has-map > div.search-wrap > div.search-contents.ml-0 > div > div:nth-child(1) > a > div.list-view-id-container.justify-content-center > div > span:nth-child(1)").text
        split = raw.upper().split(" ")
        if len(split) == 1:
            raise
        return int(split[1])

    @staticmethod
    def __replace_moth(date: str) -> str:
        replace_object = {'янв': 'jan', 'фев': 'feb', 'мар': 'mar', 'апр': 'apr', 'май': 'may', 'июн': 'jun',
                          'июл': 'jul', 'авг': 'aug', 'сен': 'sep', 'окт': 'oct', 'ноя': 'nov', 'дек': 'dec'}
        split = date.split(" ")
        if len(split) > 1:
            month = split[1].lower()
            if len(re.findall(r"[а-я]", month.lower())) != 0:
                month = replace_object[month.split(".")[0]]
            return split[0] + " " + month + " " + split[3]
        raise

    def __parse_date(self, soup: BeautifulSoup) -> datetime.datetime:
        raw_date = soup.select_one(
            "#main_block > div.d-flex.justify-content-between.p-relative.search-content.has-map > div.search-wrap > div.search-contents.ml-0 > div > div:nth-child(1) > a > div.list-view-id-container.justify-content-center > div > span.d-block.mb-3").text
        date = self.__replace_moth(raw_date).lower()
        return datetime.datetime.strptime(date, "%d %b %H:%M")

    def __parse_href(self, soup: BeautifulSoup) -> str:
        try:
            tag = soup.select_one(
                "#main_block > div.d-flex.justify-content-between.p-relative.search-content.has-map > div.search-wrap > div.search-contents.ml-0 > div > div:nth-child(1) > a")
            if tag.has_attr("href"):
                return tag.attrs["href"]
        except:
            return ""

    def parse(self, html: str) -> LastAppartment:
        soup = BeautifulSoup(html, "lxml")
        return LastAppartment(self.__parse_id(soup), self.__parse_date(soup), self.__parse_href(soup))
